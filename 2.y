%{
#include<stdio.h>
#include<ctype.h>
%}
%token A B
%%
line : line str '\n' {printf("\n Valid string\n");}
|
| error '\n' {yyerror("\n Invalid string\n"); yyerrok;};
str : A s1 B|B
s1 : | A s1;
%%
int main()
{
yyparse(); // call the rule section
}
yyerror(char *s) //built in function to display error message

{
printf("%s\n",s);
}
yylex()
{
int c;
while((c=getchar())==' '); //Accept single character and store it in c then terminate
if(c =='a' || c =='A') return A; //match input character with a or A
if(c =='b' || c =='B') return B; //match input character with b or B
return c;
}