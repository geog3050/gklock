def leaves(climate, temperature):
    if climate== "Tropical":
        for x in temperature:
            if x<=30.0:
                print("F")
                continue
            else:
                print("U")
                continue
    elif climate=="Continental":
        for x in temperature:
            if x<=25.0:
                print("F")
                continue
            else:
                print("U")
                continue
    else:
        for x in temperature:
            if x<=18.0:
                print("F")
                continue
            else:
                print("U")
                continue

    
