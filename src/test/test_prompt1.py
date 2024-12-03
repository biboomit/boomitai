from ..promptsManager.prompt1 import Prompt1

prompt = Prompt1()

res = prompt.createPrompt([["11"], ["1"], [["11"], ["11"], ["1111"]], [["111"]], [[["111"], ["111"]]]])

# prompt.createPrompt([["01"], ["1"], [["10"], ["10"], ["1000"]], [["100"]], [[["110"], ["000"]]]])

#print(res)

exit(0)



## TODO: Revisar las condiciones de obtainComponent, que creo que falta un loop/entrar un nivel mas profundo