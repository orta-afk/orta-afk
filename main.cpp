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

  for (auto& tspan : profileTextNode.children("tspan")) {
    auto idAttr = tspan.attribute("id");
    if (idAttr && std::string(idAttr.value()) == "age_data") {
        for (auto child : tspan.children()) {
            tspan.remove_child(child);
        }

        tspan.append_child(pugi::node_pcdata).set_value((std::to_string(age) + " ala").c_str());
        std::cout << "Updated: " << tspan.text().as_string() << "\n";
    }
  }


  doc.save_file("../profile.svg", PUGIXML_TEXT(""), pugi::format_no_declaration | pugi::format_raw);
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
