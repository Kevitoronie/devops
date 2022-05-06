from padaria.ext.db import db, auth

def insert_proposta(cnpj, rs, end, num, bairro, estado, cep, telfixo, telcel, email, vp, qp, idprod):
    data = {'cnpj': cnpj,
            'rs': rs,
            'end': end,
            'num': num,
            'bairro': bairro,
            'estado': estado,
            'cep': cep,
            'telfixo': telfixo,
            'telcel': telcel,
            'email': email,
            'vp':vp,
            'qp':qp
            }

    db().child('propostas').push(data)

def auth_confirm(email, psw):
    try:
        authentication = auth().sign_in_with_email_and_password(email,psw)
        return 'OKAY'
    except:
        return 'ERROR'

def send_email_reset_senha(email):
    try:
        authentication = auth().send_password_reset_email(email)
        return 'OKAY'
    except:
        return 'ERROR'

def send_email_to_cnpj(cnpj):
    id = []
    ids =  db().child('users').order_by_child('cnpj').equal_to(int(cnpj)).get()
    for i in ids.each():
        id.append(i.val()['email'])
    if len(id) == 0:
        return 'error'
    else:
        return id[0]

def info_user(email):
    id = []

    ids = db().child('users').order_by_child('email').equal_to(str(email)).get()
    for i in ids.each():
        id.append(dict(i.val()))

    if len(id) == 0:
        return 'error'
    else:
        return id[0]


#print(info_user('kvnronie@gmail.com'))
#print(send_email_to_cnpj(123))
#auth_confirm('teste@teste.com.br','kevinteste')
#insert_user(12345678910,'teste','teste',12345678910,'rua teste',12345678910,'teste','teste',542,12547,2145,'kvnronie@gmail.com.br','kevin123')
#print(get_all_products())
#get_all_products()
