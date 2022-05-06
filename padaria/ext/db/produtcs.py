from padaria.ext.db import db, storage

def save_image_produto_storage(name,id):
    storage().child(f'produto/{id}').put(name)



def delete_image_produto_storage(id):
    storage().delete(name=f'produto/{id}',token=None)

def update_product(id, title, pricemin, pricemax, quant, uniquant, cat, prefmark, localentrega, desc, foto):
    """ atualiza os dados do produto """
    data = {'id':id,
            'title':title,
            'pricemin': pricemin,
            'pricemax':pricemax,
            'quant':quant,
            'uniquant': uniquant,
            'cat':cat,
            'prefmark': prefmark,
            'localentrega': localentrega,
            'desc':desc,
            'status':'true',
            'foto': f'produto/{id}'
            }
    db().child('produtos').child(id).set(data)
    if foto != '':
        save_image_produto_storage(foto,id)

def delete_product(id):
    """ deleta o produto através da id """
    db().child('produtos').child(id).remove()
    delete_image_produto_storage(id)

#delete_product(0)
def get_category_all_products():
    """ pega todas as categorias dos produtos """

def insert_product(title, pricemin, pricemax, quant, uniquant, cat, prefmark, localentrega, desc, foto):
    """ cadastra o produto e a imagem do produto """
    try:
        id = int(get_last_id_all_produtcs()) + 1
    except:
        id=0
    data = {'id':id,
            'title':title,
            'pricemin': pricemin,
            'pricemax':pricemax,
            'quant':quant,
            'uniquant': uniquant,
            'cat':cat,
            'prefmark': prefmark,
            'localentrega': localentrega,
            'desc':desc,
            'status':'true',
            'foto': f'produto/{id}'
            }
    db().child('produtos').child(id).set(data)

    save_image_produto_storage(foto,id)

def url_image(id):
    """ pega a url da imagem """
    ulr = storage().child(id).get_url(None)
    return ulr

def get_last_id_all_produtcs():
    """pega o ultimo id de todos os produtos"""
    id = []
    ids = db().child('produtos').get()
    for i in ids.each():
        if i.val() != None:
            id.append(i.val()['id'])
    if len(id) == 0:
        return 0
    else:
        return id[len(id)-1]
get_last_id_all_produtcs()
def get_all_products(pesquisa='',filtro='Todos'):
    """pega todos os produtos, filtrando e pesqisando"""
    lp = {}
    if pesquisa != '' and filtro != 'Todos':
        produtos = db().child('produtos').get()
        if produtos.each() != None:
            for i in produtos.each():
                if i.val() != None and str(pesquisa).upper() in str(i.val()['title']).upper() and str(filtro).upper()  in str(i.val()['cat']).upper():
                    lp[str(i.val()['id'])] = dict(i.val())
            return lp
        else:
            return ""

    elif pesquisa == '' and filtro != 'Todos':
        produtos = db().child('produtos').get()
        if produtos.each() != None:
            for i in produtos.each():
                if i.val() != None and str(filtro).upper() in str(i.val()['cat']).upper():
                    lp[str(i.val()['id'])] = dict(i.val())
            return lp
        else:
            return ""

    else:
        produtos = db().child('produtos').get()
        if produtos.each() != None:
            for i in produtos.each():
                if i.val() != None and str(pesquisa).upper() in str(i.val()['title']).upper():
                    lp[str(i.val()['id'])] = dict(i.val())
            return lp
        else:
            return ""

#print(get_all_products(pesquisa=''))
#insert_product('title', 'pricemin', 'pricemax', 'quant', 'uniquant', 'prefmark', 'localentrega', 'desc')
#print(get_all_products())