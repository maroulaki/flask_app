Συμπίεση Huffman και κωδικοποίηση κυκλικού κώδικα
---
### Ομάδα:
p21095: Γιώργος Μαρμαράς

p21167: Μαρία Τιμολόγου

---

### **Αρχεία (flask_app)**:
- **client.py** (το αρχείο όπου τρέχει ο client)
- **crypto_utils.py** (βοηθητικές συναρτήσεις)
- **cyclic.py** (κωδικοποίηση και αποκωδικοποίηση με κυκλικό κώδικα)
- **huffman.py** (συμπίεση και αποσυμπίεση με Huffman)
- **message.txt** (το αρχείο με το μήνυμα που θα μεταδοθεί)
- **server.py** (το αρχείο όπου τρέχει ο server)

#### Dependencies: colorama

### Εκκίνηση
Εφόσον έχουν εγκατασταθεί τα flask και sagemath, πρώτα τρέχει το αρχείο `server.py`, το οποίο μένει ενεργό στο δικό του παράθυρο terminal. Μετά με κάποιο πρόγραμμα επεξεργασίας κειμένου μπορεί να εισαχθεί το μήνυμα που θα κωδικοποιηθεί. Έπειτα μπορεί να τρέξει σε ξεχωριστό terminal το `client.py` με παραμέτρους το μήνυμα και η τοποθεσία του σφάλματος (στο διάστημα [0,1])

```
python client.py -f message.txt -x 0.4
```
### Screenshots εκτέλεσης
`server.py`
![img](https://i.imgur.com/LzaniSU.png)

`message.txt`<br>
![img](https://i.imgur.com/Yl50RRX.png)

`client.py`
![img](https://i.imgur.com/k1E7ujD.png)
