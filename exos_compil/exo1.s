ldr r1, =a
ldr r2, =b
mov r3, #3
mov r4, #8
str r3, [r1]
str r4, [r2]
ldr r1, =a
ldr r2, =b
ldr r3, [r1]
ldr r4, [r2]
cmp r3, r4
bgt true
mov r0, #20
true:
mov r0, #10


    





