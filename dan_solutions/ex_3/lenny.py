from dataclasses import dataclass


@dataclass
class Gecko:
    name: str
    color: str

done = False
geckos: list[Gecko] = []
while done:
    name = input("what is the gecko's name ? ")
    color = input("what is the gecko's color ? ")
    if name == "done":
        done = True
    else:
        geckos.append(Gecko(name=name, color=color))

done = False
while done:
    first_gecko_name = input("first gecko to marry")
    if first_gecko_name == "done":
        done = True
        continue
    second_gecko_name = input("second gecko to marry")

    first_gecko_color = []
    print(f"Their baby gecko's color is {} and {}") 
    


