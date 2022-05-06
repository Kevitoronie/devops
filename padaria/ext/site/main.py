from flask import Blueprint
from flask import request, render_template, redirect, url_for, session, abort
from flask_login import login_manager
from padaria.ext.site import controllers
from padaria.ext.auth import main as auth
from padaria.ext.db import produtcs as db
from padaria.ext.db import users

bp = Blueprint('site', __name__)


@bp.route('/', methods=['GET','POST'])
def index():
    session.clear()
    if request.method == 'POST':
        login = request.values['username']
        senha = request.values['psw']
        if '@' not in login and login.isnumeric():
            email = controllers.send_email_to_cnpj(login)
            auth = controllers.auth_confirm(email, senha)
            infos = users.info_all(email)
            if auth == 'OKAY' and infos != 'error':
                session['FBLogin'] = infos
                session['filtro'] = 'Todos'
                session['pesquisa'] = ''
                return redirect('/produtos')
            else:
                return render_template('pages/index.html', error='CNPJ / E-mail ou senha incorretos!')
        else:
            auth = controllers.auth_confirm(login, senha)
            infos = controllers.info_user(login)
            if auth == 'OKAY' and infos != 'error':
                session['FBLogin'] = infos
                return redirect('/produtos')
            else:
                return render_template('pages/index.html', error='CNPJ / E-mail ou senha incorretos!')
    return render_template('pages/index.html')


@bp.route('/resetpw', methods=['GET','POST'])
def resetsenha():
    if request.method == 'POST':
        login = request.values['username']
        if '@' not in login and login.isnumeric():
            email = controllers.send_email_to_cnpj(login)
            auth = controllers.send_email_reset_senha(email)
            if auth == 'OKAY':
                return render_template('pages/resetpw_ok.html')
            else:
                return render_template('pages/resetpw.html', error='CNPJ / E-mail não encontrado')
        else:
            auth = controllers.send_email_reset_senha(login)
            if auth == 'OKAY':
                return render_template('pages/resetpw_ok.html')
            else:
                return render_template('pages/resetpw.html', error='CNPJ / E-mail não encontrado')

    return render_template('pages/resetpw.html')


@bp.route('/resetpw/<email>', methods=['GET','POST'])
def resetsenhaconta(email):
    if request.method == 'POST':
        login = request.values['username']
        if '@' not in login and login.isnumeric():
            email = controllers.send_email_to_cnpj(login)
            auth = controllers.send_email_reset_senha(email)
            if auth == 'OKAY':
                return render_template('pages/resetpw_ok.html', email=email)
            else:
                return render_template('pages/resetpw.html', error='CNPJ / E-mail não encontrado', email=email)
        else:
            auth = controllers.send_email_reset_senha(login)
            if auth == 'OKAY':
                return render_template('pages/resetpw_ok.html', email=email)
            else:
                return render_template('pages/resetpw.html', error='CNPJ / E-mail não encontrado', email=email)

    return render_template('pages/resetpw.html', email=email)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    campos = {'cnpj':'', 'nf':'', 'email':'', 'pw':'', 'pw_confirm':'', 'telcel':''}
    if request.method == 'POST':
        dados={}
        for i in campos:
            dados[i] = request.values[i]
        resp = auth.confirm_cadastro(**dados)
        if resp == 'OK':
            return render_template('pages/index.html', ok='Cadastro Realizado com Sucesso')
        elif resp == 'ERROR_S':
            return render_template('pages/registrar.html', error='As Senha Digitadas Não Conferem', dados=dados)
        elif resp == 'ERROR_C':
            return render_template('pages/registrar.html', error='CNPJ Invalido!',dados=dados)
    return render_template('pages/registrar.html',dados=campos)


@bp.route('/produtos', methods=['GET','POST'])
def produtos():
    if 'FBLogin' not in session:
        return abort(401)
    else:
        session['filtro'] = 'Todos'
        session['pesquisa'] = ''
        if request.method == 'POST':
            pesq = request.form['pesquisa']
            f = request.values['filtro']

            session['pesquisa'] = pesq
            session['filtro'] = f

            if pesq != '':
                prod = db.get_all_products(pesquisa=pesq, filtro=f)
            else:
                prod = db.get_all_products(filtro=f)


            if str(session['FBLogin']['admin']) == '1':
                return render_template('pages/produtos.html', empresa=session['FBLogin']['nf'], admin='1', produtos='Meus Produtos',
                                       venda='Propostas', p=prod, f=f, pesq=session['pesquisa'], filt=session['filtro'])
            else:
                return render_template('pages/produtos.html', empresa=session['FBLogin']['nf'], admin='0', produtos='Produtos',
                                       venda='Minha Prospostas', p=prod, f=f, pesq=session['pesquisa'], filt=session['filtro'])
        prod = db.get_all_products()
        if str(session['FBLogin']['admin']) == '1':
            return render_template('pages/produtos.html', empresa=session['FBLogin']['nf'], admin='1', produtos='Meus Produtos', venda='Propostas',p=prod, pesq=session['pesquisa'], filt=session['filtro'])
        else:
            return render_template('pages/produtos.html', empresa=session['FBLogin']['nf'], admin='0', produtos='Produtos', venda='Minha Prospostas',p=prod, pesq=session['pesquisa'], filt=session['filtro'])


@bp.route('/produto/editar/<int:id>', methods=['GET','POST'])
def editar(id):
    if 'FBLogin' not in session:
        return abort(401)
    else:
        if request.method == 'POST':
            form = ['title', 'pricemin', 'pricemax', 'quant', 'uniquant', 'cat', 'prefmark', 'localentrega', 'desc', 'foto']
            infos={'id':id}
            for i in form:
                if i == 'foto':
                    foto = request.files[i]
                    if foto.filename == "":
                        infos[i] = ""
                    else:
                        infos[i]=foto
                else:
                    infos[i] = request.form[i]
            db.update_product(**infos)
            return redirect('/produtos')

        prod = db.get_all_products()
        emp = session['FBLogin']
        if str(emp['admin']) == '1':
            return render_template('pages/produtos.html', empresa=emp['nf'], produtos='Meus Produtos', admin='1',
                                       venda='Propostas', p=prod, produto=prod[str(id)], mod='editar')
        else:
            return render_template('pages/produtos.html', empresa=emp['nf'], produtos='Produtos', admin='0',
                                       venda='Minha Propostas', p=prod, produto=prod[str(id)], mod='editar')

@bp.route('/produto/adicionar', methods=['GET','POST'])
def adicionar():
    if 'FBLogin' not in session:
        return abort(401)
    else:
        if request.method == 'POST':
            nome = request.form['nome']
            quant = request.form['quant']
            selectunit = request.form['selectunit']
            vmin = request.form['vmin']
            vmax = request.form['vmax']
            selectcat = request.form['selectcat']
            pmark = request.form['pmark']
            lentreg = request.form['lentreg']
            desc = request.form['desc']
            foto = request.files['foto']

            db.insert_product(nome,vmin,vmax,quant,selectunit,selectcat,pmark,lentreg,desc,foto)
            return redirect('/produtos')

        prod = db.get_all_products()
        emp = session['FBLogin']
        if str(emp['admin']) == '1':
            return render_template('pages/produtos.html', empresa=emp['nf'], admin='1' ,produtos='Meus Produtos', venda='Propostas',p=prod,mod='adicionar')
        else:
            return render_template('pages/produtos.html', empresa=emp['nf'],admin='0', produtos='Produtos', venda='Minha Prospostas',p=prod,mod='adicionar')


@bp.route('/produto/<int:id>', methods=['GET','POST'])
def modal(id):
    if 'FBLogin' not in session:
        return abort(401)
    else:

        prod = db.get_all_products()
        emp = session['FBLogin']

        if request.method == 'POST':
            vp = request.form['valorproposta']
            qp = request.form['quantproposta']
            unp = request.form.get('selectunit')
            controllers.insert_proposta(cnpj=emp['cnpj'], rs=emp['rs'], end=emp['end'], num=emp['num'], bairro=emp['bairro'],
                                        estado=emp['estado'], cep=emp['cep'], telfixo=emp['telfixo'], telcel=emp['telcel'],
                                        email=emp['email'], vp=vp, qp=f'{qp} {unp}')

            if str(emp['admin']) == '1':
                return render_template('pages/produtos.html', empresa=emp['nf'], produtos='Meus Produtos', admin='1',
                                       venda='Propostas', p=prod, produto=prod[str(id)], mod='2', msg='Proposta Enviada')
            else:
                return render_template('pages/produtos.html', empresa=emp['nf'], produtos='Meus Produtos',
                                       venda='Propostas',
                                       p=prod, produto=prod[str(id)], mod='2', msg='Proposta Enviada', admin='0')

        if str(emp['admin']) == '1':
            return render_template('pages/produtos.html', empresa=emp['nf'],admin='1',produtos='Meus Produtos',
                                   venda='Propostas',p=prod,produto=prod[str(id)],mod='1')
        else:
            return render_template('pages/produtos.html', empresa=emp['nf'],admin='0', produtos='Produtos', p=prod,produto=prod[str(id)],
                                   venda='Minha Prospostas',mod='1')


@bp.route('/produto/delete/<int:id>', methods=['GET','POST'])
def delete(id):
    if 'FBLogin' not in session:
        return abort(401)
    else:
        db.delete_product(id)
        return redirect('/produtos')


@bp.route('/minhaconta')
def minhaconta():
    if 'FBLogin' not in session:
        return abort(401)
    else:
        if str(session['FBLogin']['admin']) == '1':
            return render_template('pages/account.html', empresa=session['FBLogin']['nf'], admin='1',
                                   produtos='Meus Produtos', venda='Propostas', mod='1', dados=session['FBLogin'])
        else:
            return render_template('pages/account.html', empresa=session['FBLogin']['nf'], admin='0',
                                   produtos='Produtos', venda='Minhas Propostas', mod='1', dados=session['FBLogin'])

@bp.route('/minhaconta/editar/<int:id>', methods=['GET','POST'])
def minhaconta_editar(id):
    if 'FBLogin' not in session:
        return abort(401)
    else:
        if request.method == 'POST':
            dados={'id':id,'admin':session['FBLogin']['admin']}
            tipos = ['cnpj','end','num','cep','email','rs','telfixo','bairro','foto','nf','estado','uf','telcel']
            for i in tipos:
                if i == 'foto':
                    foto = request.files[i]
                    if foto.filename == "":
                        dados[i] = ""
                    else:
                        dados[i] = foto
                else:
                    dados[i] = request.form[i]
            print(dados)
            users.update_user(**dados)
            infos = users.info_all(session['FBLogin']['email'])
            session.clear()
            session['FBLogin'] = infos
            return redirect('/minhaconta')

        return redirect('/minhaconta')


@bp.route('/logout')
def logout():
    if 'FBLogin' not in session:
        return redirect('/')
    else:
        session.clear()
        return redirect('/')
