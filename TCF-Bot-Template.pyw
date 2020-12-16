import smtplib, ssl, requests, time
from datetime import datetime

"""
/****************| TCF-Bot |****************\

Prérequis:
- Une boite GMAIL (preferablement une boite inutile/jetable)
- Une boite email personnelle qui vous notifiera à la reception d'un email
- Python 3.8
- Beaucoup de patience

Configuration:
- Affecter l'addresse email de la boite GMAIL et son mot de passe aux variables "login" et "password" de la fnct sendEmail.
- Affecter l'addresse email de la boite personnelle à la variable "receiver" de la fnct sendEmail.
- Autoriser les applications non-sécurisées au niveau des paramètres de votre boite GMAIL.
  NOTE: google désactive automatiquement ce paramètre aprés un certain temps, il faudra donc vérifier manuellement 
        qu'il reste activé durant la durée d'utilisation du bot.
- Se connecter avec votre compte IF-Algérie et cocher la case "se souvenir de moi".
- Affecter le nom du cookie "remember_web_trucmachinchose" à la variable cookie dans sa position adéquate.
- Décoder la valeur du cookie pour remplacer les caractères de la forme "%3D" par leurs valeurs en utilisant ce site: https://meyerweb.com/eric/tools/dencoder/
- Affecter le résultat à la variable cookie.

+ IMPORTANT: Il faut impérativement fermer la page IF-Algérie sans se déconnecter.

Pour vérifier que la configuration des boites email a été effectuée correctement, commentez le code et faites appel à la fonction sendEmail sans condition.
"""

"""*************************************************"""
def difference(a, b): #fonction permettant de calculer un indice de différence entre 2 chaines
    if(a == b):
        return 0
	
    cpt=0
    u=zip(a,b)
    for i,j in u:
        if i!=j:
            cpt+=1
    return cpt/(min(len(a), len(b)))
"""*************************************************"""
def sendEmail():
	port = 465
	# Creation d'un contexte SSL sécurisé
	context = ssl.create_default_context()

	login = "" #addresse gmail d'envoi, doit avoir l'option "autoriser les applications non-sécurisées" activée
	password = "" #mot de passe de la boite gmail d'envoi
	receiver = "" #addresse email de reception, preferablement reliée à votre téléphone pour être notifié

	message = "Subject: TCF-Bot Update\nUn changement à été déctecté".encode('utf-8') #objet et corps de l'email de notification.

	with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
			server.login(login, password) #connection à la boite gmail d'envoi
			server.sendmail("TCF-Bot", receiver, message) # envoi de l'email
"""*************************************************"""
s = requests.Session()
url = 'https://portail.if-algerie.com/'
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}
cookie = {'remember_web_SOMETHINGSOMETHING': 'valeur de votre cookie remember_web'}

x = s.get(url, headers=header, cookies=cookie)
if("TCF".encode('utf-8') in x.content):
    print("Cookie valide.")
else:
    print("Cookie invalide. Veuillez vous déconnecter/reconnecter au niveau de votre navigateur et mettre à jour le cookie.")
    exit()

nbReqs = 0
nbVersions = 1
nbIgnored = 0
delay = 60*5 #vérifie une fois par 5min
print("Vérifié", nbReqs, "fois,", nbVersions, "version(s) recontrée(s) et", nbIgnored, "version(s) ignorée(s)")
while(True):
    time.sleep(delay)
    try:
        y = s.get(url, headers=header, cookies=cookie)
        nbReqs += 1
        diff = difference(x.content, y.content)
        if(diff >= 0.1): #0.1 pour ignorer les changements mineurs
            sendEmail()
            now = datetime.now()
            print(now, ": Nouvelle version détectée avec différence de", diff)
            nbVersions += 1
        elif(diff > 0):
            now = datetime.now()
            print(now, ": Nouvelle version ignorée avec différence de", diff)
            nbIgnored += 1
        x=y
    except:
        print("Une erreur est survenue, itération ignorée...")
    print("Vérifié", nbReqs, "fois,", nbVersions, "version(s) recontrée(s) et", nbIgnored, "version(s) ignorée(s)")
