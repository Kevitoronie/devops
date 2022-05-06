from padaria.ext.db import db, auth
from padaria.ext.api import main as api
from padaria.ext.db import users

def confirm_cadastro(cnpj, nf, email, pw, pw_confirm, telcel):
    infocnpj = api.consult_cnpj(cnpj)
    if infocnpj['status'] == 'OK' and infocnpj['situacao'] == 'ATIVA':
        if str(pw) == str(pw_confirm):
            auth().create_user_with_email_and_password(email,pw)
            users.insert_user(cnpj=int(cnpj),
                                rs=infocnpj['nome'],
                                nf=nf,
                                ie='',
                                end=infocnpj['logradouro'],
                                num=infocnpj['numero'],
                                bairro=infocnpj['bairro'],
                                estado=f'{infocnpj["municipio"]}',
                                uf=f'{infocnpj["uf"]}',
                                cep=str(infocnpj['cep']).replace('-','').replace('.',''),
                                telfixo=infocnpj['telefone'],
                                telcel=telcel,
                                email=email )
            return 'OK'
        else:
            return 'ERROR_S'
    else:
        return 'ERROR_C'
