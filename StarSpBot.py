# -*- coding: utf-8 -*-
"""
The bot intended to obtain data from a cloud DB.
It gets message from user, wraps it into an SQL-request, and returns the answer from the database
"""

import ibm_db
import logging as log
log.basicConfig(filename='<ПУТЬ К ВАШЕМУ ФАЙЛУ .log>',level=log.INFO, format='%(asctime)s %(message)s', datefmt='%m.%d.%Y %H:%M:%S')
import telebot

bot = telebot.TeleBot('<YOUR TOKEN HERE>')

hi_list=[]
hi_list=['hi','hello','привет','здравствуй','здравствуйте']

alltranslators='Александров;Васильев;Захаров'
Tra_list=alltranslators.split(';')

allLanguages={'eng': 'английский','deu': 'немецкий',
             'fra':'французский', 'rus':'русский',
             'ukr':'украинский', 'bel':'белорусский',
             'kat':'грузинский', 'kaz':'казахский',
             'kir':'киргизский', 'tkm':'туркменский',
             'hye':'армянский', 'dan':'датский',
             'taj':'таджикский', 'uzb':'узбекский',
             'pol':'польский', 'ita':'итальянский',
             'esp':'испанский', 'swe':'шведский',}


#having got a text message, we chech it against some conditions:

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    log.info(
            'Incoming message: '+ str(message.text) + ' from: ID '+ str(message.from_user.id) +
            ' ' + str(message.from_user.first_name) + ' @' + str(message.from_user.username ))
    mess=""
    mess = message.text.lower()
    if mess in hi_list:
        print('User wrote: ',message.text)
        bot.send_message(message.from_user.id,"Здравствуйте, {}!".format(message.chat.first_name))

    elif message.text=='/help':
        bot.send_message(message.from_user.id,
                        "Напишите язык, например, FRA, чтобы получить список тех, кто им владеет")
        bot.send_message(message.from_user.id,
                        "Напишите языковую пару, например, Rus-deu, чтобы получить список работающих с ней переводчиков")
        bot.send_message(message.from_user.id,
                        "Напишите мне фамилию переводчика, чтобы узнать о нем побольше")
        bot.send_message(message.from_user.id,
                        "Напишите /lang, чтобы получить список языков")
        print('User asked me for help')

    elif message.text in Tra_list:
        dsn='DRIVER={IBM DB2 ODBC DRIVER};DATABASE=BLUDB;HOSTNAME=<YOUR HOSTNAME>;PORT=50000;PROTOCOL=TCPIP;UID=<YOUR UID>;PWD=<YOUR PWD>'

        try:
            conn = ibm_db.connect(dsn, "", "")
            print ("Connected to database")
            #bot.send_message(message.from_user.id,"Database connection established")
        except:
            print ("Unable to connect: ", ibm_db.conn_errormsg() )
            bot.send_message(message.from_user.id,"Sorry, the database seems to be unavailable")

        selectQuery = "select * from TRANSLATORS where L_NAME like '%"+message.text+"%'"

        selectStmt2 = ibm_db.exec_immediate(conn, selectQuery)

        while ibm_db.fetch_row(selectStmt2) != False:
            print (
            " TYPE: ",  ibm_db.result(selectStmt2, 0), " Last name: ",
              ibm_db.result(selectStmt2, "L_NAME"),
               'First_name: ', ibm_db.result(selectStmt2, "F_NAME", )
               )

            bot.send_message(
            message.from_user.id, str(ibm_db.result(selectStmt2, 0))+' '+str(ibm_db.result(selectStmt2, 1))+
            ' '+str(ibm_db.result(selectStmt2,2))+' \n'+str(ibm_db.result(selectStmt2,3))+
            '\n'+str(ibm_db.result(selectStmt2,4))+'\n '+str(ibm_db.result(selectStmt2,5))
                    )
    elif mess in allLanguages.keys():
        dsn='DRIVER={IBM DB2 ODBC DRIVER};DATABASE=BLUDB;HOSTNAME=<YOUR HOSTNAME>;PORT=50000;PROTOCOL=TCPIP;UID=<YOUR UID>;PWD=<YOUR PWD>'

        try:
            conn = ibm_db.connect(dsn, "", "")
            print ("Connected to database")
            #bot.send_message(message.from_user.id,"Database connection established")
        except:
            print ("Unable to connect: ", ibm_db.conn_errormsg() )
            bot.send_message(message.from_user.id,"Sorry, the database seems to be unavailable")

        selectQuery = "select * from TRANSLATORS where LANG like '%"+mess.upper()+"%'"

        selectStmt2 = ibm_db.exec_immediate(conn, selectQuery)
        while ibm_db.fetch_row(selectStmt2) != False:
            print (
                    " TYPE: ",  ibm_db.result(selectStmt2, 0),
                     " Last name: ",  ibm_db.result(selectStmt2, "L_NAME"),
                      'First_name: ', ibm_db.result(selectStmt2, "F_NAME", )
                    )
            bot.send_message(
            message.from_user.id, str(ibm_db.result(selectStmt2,0))+' '+str(ibm_db.result(selectStmt2,1))+
            ' '+str(ibm_db.result(selectStmt2,2))+' \n'+str(ibm_db.result(selectStmt2,3))+' \n'+str(ibm_db.result(selectStmt2,4))+
            '\n'+str(ibm_db.result(selectStmt2,5))
            )
    elif len(message.text)==7 and mess[:3] in allLanguages.keys(): #Move out into a sep function
        dsn='DRIVER={IBM DB2 ODBC DRIVER};DATABASE=BLUDB;HOSTNAME=<YOUR HOSTNAME>;PORT=50000;PROTOCOL=TCPIP;UID=<YOUR UID>;PWD=<YOUR PWD>'

        try:
            conn = ibm_db.connect(dsn, "", "")
            print ("Connected to database")
            #bot.send_message(message.from_user.id,"Database connection established")
        except:
            print ("Unable to connect: ", ibm_db.conn_errormsg() )
            bot.send_message(message.from_user.id,"Sorry, the database seems to be unavailable")

        selectQuery = "select * from TRANSLATORS where LANG like '%"+mess.upper()+"%'"

        selectStmt2 = ibm_db.exec_immediate(conn, selectQuery)
        while ibm_db.fetch_row(selectStmt2) != False:
            print (
                    " TYPE: ",  ibm_db.result(selectStmt2, 0),
                     " Last name: ",  ibm_db.result(selectStmt2, "L_NAME"),
                      'First_name: ', ibm_db.result(selectStmt2, "F_NAME", )
                    )
            bot.send_message(
            message.from_user.id, str(ibm_db.result(selectStmt2,0))+' '+str(ibm_db.result(selectStmt2,1))+
            ' '+str(ibm_db.result(selectStmt2,2))+' \n'+str(ibm_db.result(selectStmt2,3))+' \n'+str(ibm_db.result(selectStmt2,4))+
            '\n'+str(ibm_db.result(selectStmt2,5)))

    elif message.text=='/lang':
        for item in allLanguages:
            code=str(item)
            code=code.upper()
            response=''
            response=allLanguages[item]+': '+code
            bot.send_message(message.from_user.id,response)

    else:
        bot.send_message(message.from_user.id,'Sorry, dear {}! \n I cannot understand you'.format(message.chat.first_name))
        bot.send_message(message.from_user.id,'I would recommend to ask for /help')
        print('User wrote: ',message.text)


bot.polling(none_stop=True,interval=0)
