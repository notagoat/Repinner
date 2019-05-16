from mastodon import Mastodon

instance = "" #Enter instance here
userid = "" #Go to your instance page and click on your @name on the right hand side the number in the url after /web/accounts is your userid

mastodon = Mastodon(
    access_token = '',
    api_base_url = instance
)

def main():
    tootdict = {}
    toots = mastodon.account_statuses(userid,pinned=True)

    i = 0

    for toot in toots:
        i += 1
        tootdict[i] = toot['id']
    iscorrect = ordercheck(tootdict)

    if iscorrect == True:
        print("Order Confirmed, Preparing to Reorder")
        print(order)
        reorder(tootdict)
    else:
        print("Please restart to continue")
        exit()

def reorder(tootdict):
    for i in order:
        print("\n")
        print(i + " : " + mastodon.status(tootdict.get(int(i)))['content'])

    confirmed = False
    print("\n")
    while confirmed == False:
        print("Is this your preferred order? [Y/N]")
        confirm = input(">: ")
        if confirm.upper() == "Y":
            confirmed = True
            print("Confirmed!")
        elif confirm.upper() == "N":
            print("Rejected order, Closing session!")
            quit()
        else:
            print("Unknown Input, Closing session!")
            quit()
        for id in tootdict.values():
            mastodon.status_unpin(id)

        for id in reversed(order):
            mastodon.status_pin(tootdict.get(int(id)))
        print("Reordering complete! Check your mastodon for the new order!")

def ordercheck(tootdict):
    for id in tootdict.keys():
        print("\n")
        print(str(id) + " : " + mastodon.status(tootdict.get(id))['content'])

    print("\n")
    print("Enter desired order using numbers on the keyboard, seperated by spaces (E.G, 1 2 3): ")
    global order
    order = input(">: ")
    order = order.split()

    #here we check for errors
    #First check for errors in uniquness
    if len(order) > len(set(order)):
        print("Please make sure each number is unique!")
        return False

    #Check if numbers too large
    for nums in order:
        if int(nums) > len(tootdict):
            print("%s is too large for pinned toots. Please check numbering and try again!" % nums)
            return False
    #check if too small
        if int(nums) <= 0:
            print("Values smaller than 1 are invalid")
            return False

    #Check length isn''t greater than tootdict length
    if len(order) > len(tootdict):
        print("Too many values entered")
        return False

    return True


if __name__ == '__main__':
    main()
