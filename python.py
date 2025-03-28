class Elev:
    def __init__(self, nume, mate, romana, biologie, istorie):
        self.nume = nume
        self.mate = mate
        self.romana = romana
        self.biologie = biologie
        self.istorie = istorie

    def calculeaza_media(self):
        
        return (self.mate + self.romana + self.biologie + self.istorie) / 4

    def afiseaza_media(self):
        
        print(f"Elevul {self.nume} are media: {self.calculeaza_media():.2f}")


nume_elev = input("Introdu numele elevului: ")
mate = float(input("Introdu nota la matematică: "))
romana = float(input("Introdu nota la limba română: "))
biologie = float(input("Introdu nota la biologie: "))
istorie = float(input("Introdu nota la istorie: "))


elev = Elev(nume_elev, mate, romana, biologie, istorie)


elev.afiseaza_media()
