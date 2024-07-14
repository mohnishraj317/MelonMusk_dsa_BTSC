class Friend:
    def __init__(self, name, followers):
        self.name = name
        self.followers = followers

    def update(self, new_followers):
        self.followers += new_followers

def get_followers(self):
    return self.followers
    
def get_most_influential_friends(friends):
    friends.sort(key=get_followers, reverse=True)
    return friends[:4]

def main():
    friends = [
        Friend("Rahul", 996),
        Friend("Seema", 5147),
        Friend("Shaily", 5601),
        Friend("Sanjay", 451),
        Friend("Sameer", 364),
        Friend("Abhijeet", 996),
        Friend("Rakesh", 1454),
        Friend("Aparajita", 2547),
        Friend("Ganesh", 259),
        Friend("Fatima", 807)
    ]

    friends[1].update(258)  
    friends[0].update(1000)  
    friends[5].update(502)  

    friends.append(Friend("Abhiraj", 5478))
    friends.append(Friend("Bala", 1574))

    influential_friends = get_most_influential_friends(friends)

    print("The most influential friends are:")
    for friend in influential_friends:
        print(friend.name)

if __name__ == "__main__":
    main()
