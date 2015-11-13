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

 *Ceci est un exemple de réponse. Merci d'effacer ce paragraphe (mais de laisser les groupes de trois tirets et les lignes vides avant et après eux) lorsque vous y écrirez la vôtre.*

---

### Question 2

Expliquez le principe des *scopes* permettant de stocker les déclarations et la manière dont on utilise les *scopes* dans Tiger.

---

---

### Question 3

À quoi correspond la forme canonique de la représentation intermédiaire (*IR*) ? Quelle est son intérêt ?

---

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

---

## Génération de code / Conventions d'appel

### Question 5

- Qu'est-ce qu'une architecture Load / Store ?
- Quelles implications a-t-elle sur l'accès à des variables en mémoire en termes de performances ?

---

---

### Question 6

- Donnez deux exemples d'utilisations légitimes de `goto` en C
- Comment un `goto` en C sera-t-il traduit en assembleur ARM ?

---

---

### Question 7

À quoi servent le prologue et l'épilogue d'une fonction ?

---

---

### Question 8

Que contient typiquement l'activation record d'une fonction en Tiger ?

---

---

### Question 9

À quoi sert le *Frame Pointer* ? Est-il toujours nécessaire ? Motivez votre réponse en donnant au moins un exemple.

---

---

### Question 10

Comment procéder pour qu'une fonction retourne une valeur trop grosse pour tenir dans un ou deux registres (une structure, par exemple) ?

---

---

### Question 11

Quelle est la différence entre le *static link* et le *dynamic link* ?

---

---

### Question 12

En utilisant l'ABI ARM vue en cours, dans la fonction C suivante, comment sont passés les arguments ? Si des arguments sont placés sur la pile, précisez lesquels et le *layout* de la pile.

``` c
int foo(long long a, char b, int c, int d, int *e, char f);
```

---

---

### Question 13

À quoi sert cette construction assembleur ARM ?

``` asm
bx lr
```

---

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

---

### Question 16

Expliquez comment la pseudo instruction suivante est convertie en instructions assembleur en fonction de la valeur de `cste`.

``` asm
ldr r0, =cste

```

---

---

### Question 17

L'instruction: `push {r0-r3,r6-r7}`{.asm} permet de sauvegarder le contenu de registres sur la pile.

   1. Quel est la convention utilisée pour la pile des processeur ARM ?
   2. Quels registres seront sauvegardés après l'exécution de l'instruction ?
   3. Donnez une autre écriture de cette même instruction faisant apparaitre le pointeur de pile `sp`

---

---

### Question 18

Dans une boucle de calcul le registre `r0` est incrémenté en utilisant l'instruction suivante:

```asm
adds r0, r0, #1
```

Dans quelle partie de la mémoire sera sauvegardée la valeur immédiate `1` ?

---

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

---

### Question 20

Donnez le code assembleur pour ARM d'une fonction permettant de mettre à zéro (0) `n` octets d'un tableau. L'adresse de base du tableau se trouve déjà dans `r0` et le nombre d'éléments dans `r1`

---

---
