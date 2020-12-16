# Auteurs : L. Gaboriau, C. Chevreuil
# Creation : 10/11/2020
# Modification : 01/12/2020
# Projet tuteuré M. GIRAUDO - arbres pré-lie

from copy import deepcopy


def node():
        return []

def attach(*f):
    return[*f]

def get(tree, i):
    assert(0 <= i < len(tree))
    return tree[i]

def max(val1, val2):
    '''
    Retourne la plus grande valeur entre val1 et val2.

    >>> max(1, 3)
    3
    >>> max(4, 4)
    4
    >>> max(-5, 4)
    4
    >>> max(4, 0)
    4
    >>> max(-8, 0)
    0
    >>> max(-7, -2)
    -2
    '''
    if(val1 > val2):
        return val1
    return val2


def height_tree(tree):
    '''
    Retourne la hauteur de tree passé en parametre.

    >>> height_tree([])
    0
    >>> height_tree([[]])
    1
    >>> height_tree([[], []])
    1
    >>> height_tree([[], [[]]])
    2
    >>> height_tree([[[]], []])
    2
    '''
    height = -1

    if(type(tree) != list):
        return 0

    for elem in tree:
        height = max(height, height_tree(elem))

    return (height + 1)

def sort_tree_height(tree):
    '''
    Trie un arbre et le transforme en un arbre gauche
    modifie tree
    '''
    tree.sort(key=height_tree, reverse=True)
    for elem in tree:
        sort_tree_height(elem)

def equal_tree(tree1, tree2):
    '''
    Retourne True si les deux arbres quelconques tree1 et tree2
    sont égaux, False sinon.
    Ne modifie pas tree1 ni tree2

    >>> equal_tree([], [])
    True
    >>> equal_tree([[]], [])
    False
    >>> equal_tree([], [[]])
    False
    >>> equal_tree([[], []], [[], []])
    True
    >>> equal_tree([[[]], []], [[], [[]]])
    True
    '''

    if(len(tree1) != len(tree2)):
        return False

    copy_tree1 = deepcopy(tree1)
    copy_tree2 = deepcopy(tree2)

    sort_tree_height(copy_tree1)
    sort_tree_height(copy_tree2)
    
    return equal_sorted_tree(copy_tree1, copy_tree2)


def equal_sorted_tree(tree1, tree2):
    '''
    Appelée par equalTree(tree1, tree2)
    Retourne True si les deux arbres gauches tree1 et tree2
    sont égaux.
    Ne modifie pas tree1 ni tree2

    >>> equal_sorted_tree([], [])
    True
    >>> equal_sorted_tree([[]], [])
    False
    >>> equal_sorted_tree([], [[]])
    False
    >>> equal_sorted_tree([[], []], [[], []])
    True
    >>> equal_sorted_tree([[[]], []], [[], [[]]])
    False
    '''

    if(len(tree1) != len(tree2)):
        return False
    
    for i in range(len(tree1)):
        if(equal_sorted_tree(tree1[i], tree2[i]) == False):
            return False

    return True


def nb_node(tree):
    '''
    Retourne en le nombre de noeuds contenus dans l'arbre
    tree passé en parametre.
    sum = len(tree) + 1, le +1 permet de compter la racine.
    sum += (nbNode(elem) - 1), le -1 permet de rectifier la ligne du 
    dessus lorsque qu'il ne s'agit pas de la racine.

    >>> nb_node([])
    1
    >>> nb_node([[]])
    2
    >>> nb_node([[], []])
    3
    '''
    result = 1

    for elem in tree:
        result += (nb_node(elem))
    
    return result

def write_head_file(file):
    '''
    Ecrit l'en-tête du fichier .dot dans le fichier file
    '''

    file.write("digraph  arbre {\n\tnode [shape=record , height=.1 ]\n\tedge [tailclip=false , arrowtail = dot , dir=both];\n")


def write_tree_file(file, tree):
    '''
    Ecrit l'arbre tree dans le fichier file au format .dot
    '''

    file.write("\t" + str(id(tree)) + " [label= \"<empty>\"];\n")

    for i in range(len(tree)):
        file.write("\t" + str(id(tree)) + " : empty:c -> " + str(id(tree[i])) + ":empty;\n")
        write_tree_file(file, tree[i])


def write_end_file(file):
    '''
    Ecrit la fin du fichier .dot dans le fichier file
    '''

    file.write("}")


def save_tree_file(file_name, tree):
    '''
    Sauvegarde en format {fileName}.dot, l'arbre tree passé en parametre.
    '''

    file = open(str(file_name), "w+")

    write_head_file(file)
    write_tree_file(file, tree)
    write_end_file(file)

    file.close()


def save_tree_list_file(file_name, tree_list, boolean_graft = False):
    '''
    Sauvegarde dans le fichier {fileName}.dot au format .dot
    la liste de tous les arbres contenus dans treeList.
    '''

    for i in range(len(tree_list)):
        name = str(file_name)+"-"+str(i)+".dot"
        if boolean_graft :
            save_tree_file(name, tree_list[i])
        else :
            save_tree_file(name, tree_list[i][0])


def boolean_graft(tree1, tree2, current = None, tree_list = []):
    '''
    Retourne la liste de tous les arbres différents générés par une greffe pré-lie.
    "tree1" est l'arbre sur lequel "tree2" se greffe. "current" est la position courante
    dans "tree1", "treeList" est la liste des tous les arbres déjà constitués suite
    a la greffe de "tree2" sur "tree1".
    Ne modifie ni "tree1", ni "tree2".
    
    >>> boolean_graft([], [[], []])
    [[[[], []]]]
    >>> boolean_graft([[], []], [])
    [[[], [], []], [[[]], []]]
    >>> boolean_graft([], [])
    [[[]]]
    >>> boolean_graft([[[], []], []], [])
    [[[[], []], [], []], [[[], [], []], []], [[[[]], []], []], [[[], []], [[]]]]
    '''

    if(None == current):
        current = tree1

    new_tree_list = []

    current.append(tree2)
    tree_copy = deepcopy(tree1)
    current.pop()

    sort_tree_height(tree_copy)
    if(tree_copy not in tree_list):
        new_tree_list.append(tree_copy)

    for elem in current:
        new_tree_list += boolean_graft(tree1, tree2, elem, new_tree_list)

    return new_tree_list


def graft(tree1, tree2, current = None, tree_list = []):
    '''
    Retourne la liste de tous les arbres différents générés par une greffe pré-lie.
    "tree1" est l'arbre sur lequel "tree2" se greffe. "current" est la position courante
    dans "tree1", "treeList" est la liste des tous les arbres déjà constitués suite
    a la greffe de "tree2" sur "tree1".
    Ne modifie ni "tree1", ni "tree2".

    >>> graft([], [[], []])
    [([[[], []]], 1)]
    >>> graft([[], []], [])
    [([[], [], []], 1), ([[[]], []], 2)]
    >>> graft([], [])
    [([[]], 1)]
    >>> graft([[[], []], []], [])
    [([[[], []], [], []], 1), ([[[], [], []], []], 1), ([[[[]], []], []], 2), ([[[], []], [[]]], 1)]
    '''
    exists = False

    if(None == current):
        current = tree1

    new_tree_list = []

    current.append(tree2)
    tree_copy = deepcopy(tree1)
    current.pop()

    sort_tree_height(tree_copy)
    for i in range(len(tree_list)):
        if tree_copy == tree_list[i][0]:
            exists = True
            temp = list(tree_list[i])
            temp[1] += 1
            tree_list[i] = tuple(temp)
            
    if not exists :
        new_tree_list.append((tree_copy, 1))

    for elem in current:
        new_tree_list += graft(tree1, tree2, elem, new_tree_list)

    return new_tree_list

def prelie_product_tree(tree1, tree2, coef):
    '''
    Retourne le produit des deux arbres pre-lie
    tree1 et tree2. Coef est le coefficient polynomial
    de tree1 multiplié par le coefficient polynomial de tree2
    '''
    temp = graft(tree1, tree2)
    result = []

    for elem in temp:
        result.append(tuple([elem[0], elem[1]*coef]))
    
    return result

def prelie_simplifier(prelie):
    '''
    Prend un polynome d'arbres, et additionne les doublons
    Ne modifie pas le polynome d'arbres prelie
    '''
    result = []

    for elem in prelie:
        placed = False

        for i in range(len(result)):
            if equal_tree(result[i][0], elem[0]):
                placed = True
                tempo = list(result[i])
                tempo[1] += elem[1]
                result[i] = tuple(tempo)
                break
        
        if not placed:
            result.append(elem)

    return result

def prelie_product_polynomial(prelie1, prelie2):
    '''
    Retourne le produit de deux arbres pre-lie
    Dans un premier temps faire la multiplication de tous les arbres
    puis faire une réduction en comparant chaque arbres aux autres
    '''
    result = []

    #Produit de deux polynomes
    for tree1 in prelie1:
        for tree2 in prelie2:
            result += prelie_product_tree(tree1[0], tree2[0], tree1[1]*tree2[1])
    
    #Addition des doublons
    return prelie_simplifier(result)

def sum_polinomial(prelie1, prelie2):
    '''
    Retourne la somme des deux polynomes d'arbres prelie1 et prelie2.
    Ne modifie ni prelie1 ni prelie2
    '''
    tempo = []

    tempo += prelie1
    tempo += prelie2

    return prelie_simplifier(tempo)

def coef_polynomial(list_tree, tree):
    '''
    Retourne le coefficient de tree dans list_tree. 
    Si tree ne fait pas partie de list_tree, retourne 0
    '''
    for i in range(len(list_tree)):
        if(equal_tree(list_tree[i][0], tree)):
            return list_tree[i][1]
        
    return 0

"""
def tree_gen_node(nb_nodes, tree = None):
    '''
    retourne la liste de tous les arbres possibles contenant exactement nb_nodes
    '''
    if nb_nodes == 0:
        return tree_lst
    
    tree = node()
    for i in range(nb_node - 1):
        tree_lst += tree_gen_node(nb_nodes - 1, )
"""
#import doctest
#doctest.testmod(verbose="true")

tree = node()
tree2 = attach(node(), node())
tree3 = [[], [[], [[[]]]], [[[], []], []]]

print("Arbre trié")
sort_tree_height(tree3)
print(tree3)

prelie1 = graft(tree2, tree)
prelie2 = graft(tree, tree2)

print("prelie1 : "+str(prelie1))
print("prelie2 : "+str(prelie2))
#print(prelie_product_polynomial(prelie1, prelie2))

sum1 = [([[[]], []], 5), ([], 3), ([], 2), ([[], [[]]], 2)]
sum2 = [([], 2)]
print(sum_polinomial(sum1, sum2))


test1 = [([[]], 3)]
test2 = [([], 5)]
test3 = prelie_product_polynomial(test1, test2)
print("test : "+str(test3))
'''
A faire:
[X] Représentaiton arbre -> Listes
[X] Affichage -> dot
[X] Calculer hauteur arbres
[X] Calculer taille (nb Noeuds)
[X] Représentation canonique -> arbre gauche
[X] Comparaison/égalité
[X] greffe pré-lie

Après réunion du 26 novembre
[X] utiliser sorted avec une option pour trier selon la hauteur
[X] revoir la fonction nbNode
[X] changer graft en booleanGraft
[X] faire une fonction graft qui tient compte de la multiplicité
[X] Produit polynomiale prélie
[X] Simplifieur d'arbres
[X] Retourner coef polynomial d'un arbre
[X] Retourner la somme polynomiale de deux polynomes d'arbres
[ ] faire une version non-mutable
[ ] génération d'arbre selon un nombre de noeuds 
[ ] génération d'arbre selon une hauteur                                -> infinité de fils pour chaque noeuds
[X] fournir une interface / type de donnée abstrait


Question:
Combien d'abres différents qui possèdent n noeuds?
(Attention aux arbres canoniquement égaux)

Commande dot:
dot -Tpdf arbre.dot -o arbre.pdf
'''