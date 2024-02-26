import streamlit_authenticator as stauth  # pip install streamlit-authenticator


list_usernames = ['jsmith@gmail.com', 'rbriggs@gmail.com']
list_email = ['jsmith@gmail.com', 'rbriggs@gmail.com']
list_name = ['John Smith', 'Rebecca Briggs']
list_passwords = ["xx12", "xx34"]
list_passwords = stauth.Hasher(list_passwords).generate()
list_emails_prehautorized = ['melsby@gmail.com']
list_value_cookies = [30, 'random_signature_key', 'random_cookie_name']

def autentificator_list_dict(list_usernames_, list_email_, list_name_, list_passwords_, list_emails_prehautorized_, list_value_cookies_):
    list_user = ['email', 'name', 'password']
    list_cookies = ['expiry_days', 'key', 'name']
    list_value_prehautorized = {'emails': list_emails_prehautorized_}

    # generation user list
    l_user_values = []
    for n in range ( len ( list_user ) - 1 ):
        l_user_values.append ( [list_email_[n], list_name_[n], list_passwords_[n]] )

    # list to dict
    usernames = {}
    cookie = {'cookie': dict ( zip ( list_cookies, list_value_cookies_ ) )}
    prehautorized = {'preauthorized': list_value_prehautorized}

    for n in range ( len ( list_usernames_ ) ):
        usernames[list_usernames_[n]] = dict ( zip ( list_user, l_user_values[n] ) )

    usernames = {'usernames': usernames}
    config = {'credentials': usernames, **cookie, **prehautorized}  # merge dict
    return config

def get_config():
    config = autentificator_list_dict(list_usernames,list_email,list_name,list_passwords,list_emails_prehautorized,list_value_cookies)
    return config

def get_authenticator():
    config = get_config()
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['preauthorized']
    )

    return authenticator
