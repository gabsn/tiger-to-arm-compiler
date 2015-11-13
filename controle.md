% Contrôle de connaissances SE202 "Compilation"
% 13 novembre 2015

# Instructions

Ce contrôle de connaissances est strictement individuel. Vous devez modifier ce fichier pour y inclure vos réponses. Seules les parties entre *---* sont à modifier.

Les questions ont été regroupées par thèmes. Chaque question est indépendante, et il devra y être répondu de la manière la plus professionnelle et synthétique possible.

Lorsque des questions sont liées à l'architecture et aux conventions d'appel sous-jacentes, on supposera qu'on utilise un processeur ARM 32 bits avec la convention EABI.

# Questions

## Processus de compilation

### Question 1

Quelles sont les différentes étapes de la compilation ?

 ---

 1/ La première étape consiste à récupérer et à identifier les caractérès qui forment le code. On utilise pour cela un tokenizer qui est sensé reconnaître les caractères et à leur associér un label (FOR par exemple).

 2/ Ensuite il faut reconnaître la syntaxe du langage. Pour cela on utilise le parser dans lequel on a spécifié la grammaire du langage. Cela nous permet de construire un arbre composé de noeuds du langage.

 3/ On obtient alors un AST qu'il faut "binder" et "typer" afin de pouvoir par exemple gérer les appels de fonctions et les déclarations de variables.

 4/ On transforme ensuite cet AST décoré en IR (Intermediate Representation) qui est un arbre plus proche du langage assembleur.

 5/ Enfin on transforme l'IR en langage assembleur, puis en code machine qui sera lu et exécuté par le processeur.

 ---

### Question 2

Expliquez le principe des *scopes* permettant de stocker les déclarations et la manière dont on utilise les *scopes* dans Tiger.

---

Les scopes permettent d'associer à chaque variable son domaine d'existence par un système de profondeur. Cela permet notamment de vérifier qu'on ne déclare pas deux fois la même variable dans un même scope.

---

### Question 3

À quoi correspond la forme canonique de la représentation intermédiaire (*IR*) ? Quelle est son intérêt ?

---

L'IR correspond à un arbre simplifié permettant une traduction plus simple de ses noeuds en langage assembleur.

---

### Question 4

On souhaite ajouter le mot-clé `continue` dans Tiger. Il permet, lors d'une boucle, de sauter directement à l'itération suivante de la boucle.

Par exemple, le code suivant affichera "1245".

``` tiger
for i := 1 to 5 do
  (
    if i == 3 then continue;
    print_int(i)
  )
```

Expliquez en quelques mots comment vous implémenteriez le mot-clé `continue` en Tiger, qui permet, lorsqu'on est à l'intérieur d'une boucle, de revenir au début de la boucle. À quelle étapes du processus faudra-t-il intervenir ?

---

Il faudra intervenir dans le parser pour pouvoir ajouter le mot-clé 'continue' à la syntaxe du langage. Il faudra également modifier le binder afin de pouvoir revenir  au début de la boucle lorsque l'on visitera le noeud associé au mot-clé 'continue'. Enfin il faudra modifier le dumper pour ne dire de rien afficher lorsqu'il rencontrera le mot-clé 'continue'.
---

## Génération de code / Conventions d'appel

### Question 5

- Qu'est-ce qu'une architecture Load / Store ?
- Quelles implications a-t-elle sur l'accès à des variables en mémoire en termes de performances ?

---

L'architecture Load / Store implique qu'on ne puisse pas manipuler directement les données en mémoire. Il faut donc d'abord les charger dans les registres du processeur avant de pouvoir les manipuler.
Cette architecture à l'inconvénient d'avoir un impact négatif en termes de performances pour l'accès mémoire des variables en mémoire. Cependant, elle a l'avantage d'avoir des instructions plus simples.

---

### Question 6

- Donnez deux exemples d'utilisations légitimes de `goto` en C
- Comment un `goto` en C sera-t-il traduit en assembleur ARM ?

---

Le 'goto' se traduit par un b (branchement à une adresse) ou un bx (branchement à un registre) en assembleur ARM.

---

### Question 7

À quoi servent le prologue et l'épilogue d'une fonction ?

---

---

### Question 8

Que contient typiquement l'activation record d'une fonction en Tiger ?

---

L'activation record contient les variables locales et les arguments de la fonction.

---

### Question 9

À quoi sert le *Frame Pointer* ? Est-il toujours nécessaire ? Motivez votre réponse en donnant au moins un exemple.

---

Le Frame Pointer permet de délimiter le "haut" de l'espace mémoire sur la pile alloué à une fonction (un accès aux variables locales peut donc se faire en [fp + 4] par exemple). Il n'est pas toujours nécessaire, par exemple lorsque nous n'appelons pas de fonctions ou plus généralement lorsque les appels de fonction ne sont pas imbriqués.

---

### Question 10

Comment procéder pour qu'une fonction retourne une valeur trop grosse pour tenir dans un ou deux registres (une structure, par exemple) ?

---

Dans ce cas on stocke généralement la donnée sur deux registres consécutifs (si il faut 64 bits par exemple).

---

### Question 11

Quelle est la différence entre le *static link* et le *dynamic link* ?

---

Le Static Link d'une fonction pointe vers la fonction qui l'a déclaré tandis que le Dynamic Link pointe vers la fonction qui l'a appelé.

---

### Question 12

En utilisant l'ABI ARM vue en cours, dans la fonction C suivante, comment sont passés les arguments ? Si des arguments sont placés sur la pile, précisez lesquels et le *layout* de la pile.

``` c
int foo(long long a, char b, int c, int d, int *e, char f);
```

---

(registres caller-saved)
a est passé sur r_0 et r_1 car il fait 64 bits.
b est passé sur r_2.
c est passé sur r_3.
(registres calle_saved)
d, e et f sont passés sur la pile.

---

### Question 13

À quoi sert cette construction assembleur ARM ?

``` asm
bx lr
```

---

C'est la construction usuelle pour revenir de l'appel d'une fonction. La construction mov pc, lr est dépréciée car elle ne met pas à jour les retenues.

---

### Question 14

Dans notre architecture (Cortex-M), le type `int` a la même taille que les registres du processeur (32 bits), et le type `int8_t` a une taille de 8 bits.

Dans une boucle `for`, pourquoi vaut-il souvent mieux utiliser une variable d'indice de boucle de type `int` plutôt que du type `int8_t` ?

---

---

## Assembleur ARM

### Question 15

Expliquez brièvement la différence entre jeu d'instruction et directives d'assemblage.

---

Le jeu d'instruction est l'ensembles des instruction correspondant à du code machine directement exécutable par le processeur tandis que les directives d'assemblage sont seulement destinées à l'assembleur qui les transforme en code machine compréhensible par le processeur après coup (ex: pour gérer les labels, les variable .word, etc.).

---

### Question 16

Expliquez comment la pseudo instruction suivante est convertie en instructions assembleur en fonction de la valeur de `cste`.

``` asm
ldr r0, =cste

```

---

Il y a calcul assez compliqué (dont je ne me rappelle plus) pour déterminé si une valeur immédiate peut être directement mise dans un registre. Si la valeur est compatible, l'assembleur traduira l'instruction en :
            ldr r0, #cste

Sinon, il la traduira en :

            ldr r0, [pc, offset]
            ...
            .word cste

---

### Question 17

L'instruction: `push {r0-r3,r6-r7}`{.asm} permet de sauvegarder le contenu de registres sur la pile.

   1. Quel est la convention utilisée pour la pile des processeur ARM ?
   2. Quels registres seront sauvegardés après l'exécution de l'instruction ?
   3. Donnez une autre écriture de cette même instruction faisant apparaitre le pointeur de pile `sp`

---

1. La convention utilisée pour la pile des processeurs ARM est une pile qui descend vers le bas (FD).
2. Les registres sauvegardés sur la pile sont : r0, r1, r2, r3, r6 et r7.
3. str {r0-r3,r6-r7}, [sp]

---

### Question 18

Dans une boucle de calcul le registre `r0` est incrémenté en utilisant l'instruction suivante:

```asm
adds r0, r0, #1
```

Dans quelle partie de la mémoire sera sauvegardée la valeur immédiate `1` ?

---

Elle sera sauvegardée après les instructions assembleur.

---

### Question 19

Expliquez ce que fait le code assembleur suivant:

```asm
.global foo

foo:
   ldr r0, L1
   ldr r1, [r0]
   add r1, r1, #1
   str r1, [r0]
   bx lr
   nop @ nop is equivalent to mov r0,r0

L1:
   .word 0xABCD0000
```

---

Le code suivant charge la valeur de L1 (qui est une adresse) dans le registre r0, charge la valeur donnée par cette adresse dans le registre r1 puis l'incrémente de 1. Enfin il réécrit cette nouvelle valeur à l'adresse initiale.

Conclusion : ce code assembleur incrémente de 1 la valeur donnée à l'adresse 0xABCD0000.

---

### Question 20

Donnez le code assembleur pour ARM d'une fonction permettant de mettre à zéro (0) `n` octets d'un tableau. L'adresse de base du tableau se trouve déjà dans `r0` et le nombre d'éléments dans `r1`

---

start:
ldr r2, #0
ldr r3, #1
str r2, [r0]
subs r1, r1, r3
beqz start

---
