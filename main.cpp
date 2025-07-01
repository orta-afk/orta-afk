#include <iostream>
#include <pugixml.hpp>
#include <chrono>

int getBday();

int main(){
  int age = getBday();
  pugi::xml_document doc;
  pugi::xml_parse_result res = doc.load_file("../profile.svg");
  if(!res){
    std::cout << "fuck" << res.description() << std::endl;
  }
  auto rootNode = doc.child("svg");
  auto asciiTextNode = rootNode.child("text");
  auto profileTextNode = asciiTextNode.next_sibling();

  for (auto& textNode : profileTextNode.children()) {
      auto uptime = textNode.find_child_by_attribute("id", "age_data");
      if (uptime) {
          for (auto child : uptime.children()) {
              uptime.remove_child(child);
          }

          uptime.append_child(pugi::node_pcdata).set_value((std::to_string(age) + " years").c_str());
          std::cout << uptime.text().as_string();
      }
  }

  doc.save_file("../profile.svg");
  return 0;
}

int getBday(){
  int bday = 2007;
  auto now = std::chrono::system_clock::now();
  std::time_t t = std::chrono::system_clock::to_time_t(now);
  std::tm *now_tm = std::localtime(&t);
  int year = now_tm->tm_year + 1900;
  int res = year - bday;
  return res;
}
