from padaria.ext.db import db, auth, storage

def get_last_id_all_users():
    """pega o ultimo id de todos os produtos"""
    id = []
    ids = db().child('users').get()
    if ids.each() != None:
        for i in ids.each():
            if i.val() != None:
                id.append(i.val()['id'])
        if len(id) == 0:
            return 0
        else:
            return id[len(id)-1]
    return 0


def insert_user(cnpj, rs, nf, ie, end, num, bairro,uf, estado, cep, telfixo, telcel, email):
    id=get_last_id_all_users()
    data = {'id':id,
            'cnpj':cnpj,
            'rs':rs,
            'nf': nf,
            'ie':ie,
            'end': end,
            'num': num,
            'bairro': bairro,
            'estado':estado,
            'cep':cep,
            'telfixo': telfixo,
            'telcel': telcel,
            'email': email,
            'uf':uf,
            'admin': 0,
            'urlimage':"0"
            }
    db().child('users').child(id).set(data)

def save_image_account(foto, id):
    """salva a imagem e retorna o URL da foto"""
    if foto == '':
        url = storage().child(f'client/{id}').get_url(None)
        return url
    else:
        storage().child(f'client/{id}').put(foto)
        url = storage().child(f'client/{id}').get_url(None)
        return url

def update_user(id,cnpj,end,num,cep,email,rs,telfixo,bairro,foto,nf,estado,uf,telcel,admin):
    """ atualiza os dados do Usuário """
    url = save_image_account(foto,id)
    data = {'cnpj':cnpj,
            'rs':rs,
            'nf': nf,
            'ie':0,
            'end': end,
            'num': num,
            'bairro': bairro,
            'estado':estado,
            'cep':cep,
            'telfixo': telfixo,
            'telcel': telcel,
            'email': email,
            'uf':uf,
            'urlimage':url,
            'admin':admin,
            'id':id}
    db().child('users').child(id).set(data)

def info_all(email):
    id = []
    ids = db().child('users').order_by_child('email').equal_to(str(email)).get()
    for i in ids.each():
        id.append(dict(i.val()))

    if len(id) == 0:
        return 'error'
    else:
        return id[0]
