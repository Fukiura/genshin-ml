class CustomPrints:
    def __init__(self) -> None:
        pass
        
    def consolePrint(*msgs: object, startString: str = "", endString: str = "", commaModifier:str = " ") -> None:
        r""" 
            Customized print, used for the console interface and python's terminal

            startString appends before the output

            endString appends after the output
            
            commaModifier changes the way the set of msgs joined together:
                consolePrint("banana", "apple", commaModifier = "\n"); output: "banana\napple"
        """
        stringMsg = startString + commaModifier.join(map(str, msgs)) + endString
        print(stringMsg)
