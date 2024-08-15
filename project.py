class Concept:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name


class Existential:
    def __init__(self, role, concept):
        self.role = role
        self.concept = concept

    def __repr__(self):
        return f"∃{self.role}.{self.concept}"


class Conjunction:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return f"{self.left} ⊓ {self.right}"


class Subsumption:
    def __init__(self, sub, sup):
        self.sub = sub
        self.sup = sup

    def __repr__(self):
        return f"{self.sub} ⊑ {self.sup}"


def normalize(tbox):
    normalized_tbox = []
    for axiom in tbox:
        if isinstance(axiom.sup, Conjunction):
            normalized_tbox.append(Subsumption(axiom.sub, axiom.sup.left))
            normalized_tbox.append(Subsumption(axiom.sub, axiom.sup.right))
        elif isinstance(axiom.sub, Conjunction):
            normalized_tbox.append(Subsumption(axiom.sub.left, axiom.sup))
            normalized_tbox.append(Subsumption(axiom.sub.right, axiom.sup))
        else:
            normalized_tbox.append(axiom)
    return normalized_tbox


def get_name(concept):
    if isinstance(concept, Concept):
        return concept.name
    elif isinstance(concept, Existential):
        return f"∃{concept.role}.{get_name(concept.concept)}"
    elif isinstance(concept, Conjunction):
        return f"({get_name(concept.left)} ⊓ {get_name(concept.right)})"
    else:
        raise ValueError("Unknown concept type")


def entails(tbox, target):
    subsumptions = {(get_name(axiom.sub), get_name(axiom.sup)) for axiom in tbox}
    while True:
        new_subsumptions = set(subsumptions)
        for (a, b) in subsumptions:
            for (c, d) in subsumptions:
                if b == c:
                    new_subsumptions.add((a, d))
        if new_subsumptions == subsumptions:
            break
        subsumptions = new_subsumptions
    return (get_name(target.sub), get_name(target.sup)) in subsumptions


# 定义概念和角色
A = Concept("A")
B = Concept("B")
C = Concept("C")
D = Concept("D")
r = "r"
s = "s"

# 定义TBox
tbox = [
    Subsumption(A, Conjunction(B, Existential(r, C))),
    Subsumption(C, Existential(s, D)),
    Subsumption(Conjunction(Existential(r, Existential(s, Concept("⊤"))), B), D)
]

# 规范化TBox
normalized_tbox = normalize(tbox)

# 进一步规范化多次，直到没有新的规范化规则应用
while True:
    new_normalized_tbox = normalize(normalized_tbox)
    if len(new_normalized_tbox) == len(normalized_tbox):
        break
    normalized_tbox = new_normalized_tbox

# 检查是否 A ⊑ D
target = Subsumption(A, D)
result = entails(normalized_tbox, target)

# 输出结果
print("规范化后的TBox:")
for axiom in normalized_tbox:
    print(axiom)

print("\nA ⊑ D 是否成立:", result)
