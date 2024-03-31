# ba_meta require api 7
from __future__ import annotations
from typing import TYPE_CHECKING

import ba, _ba, os, random, json
from ba._activity import Activity
from bastd.actor.bomb import Bomb
from bastd.gameutils import SharedObjects
from bastd.mainmenu import MainMenuActivity
from bastd.actor.playerspaz import PlayerSpaz
from bastd.actor.spazfactory import SpazFactory

import bastd.actor.popuptext as ptext
import bastd.actor.text as text
import bastd.actor.image as image
import bastd.actor.spaz as spaz

if TYPE_CHECKING:
    from typing import Sequence, Any, Callable

class Lang:
    def __init__(self,
                 text: str,
                 subs: str | list[str] = 'none'):
        
        icons = [ba.charstr(ba.SpecialChar.CROWN),
                 ba.charstr(ba.SpecialChar.LOGO)]
 
        lang = _ba.app.lang.language
        setphrases = {
            "Installing":
                {"Spanish": f"Instalando <{__name__}>",
                 "English": f"Installing <{__name__}>",
                 "Portuguese": f"Instalando <{__name__}>"},
            "Installed":
                {"Spanish": f"¡<{__name__}> Se instaló correctamente!",
                 "English": f"<{__name__}> Installed successfully!",
                 "Portuguese": f"<{__name__}> Instalado com sucesso!"},
            "Make Sys":
                {"Spanish": "Se creó la carpeta sys",
                 "English": "Sys folder created",
                 "Portuguese": "Pasta sys criada"},
            "Restart Msg":
                {"Spanish": "Reiniciando...",
                 "English": "Rebooting...",
                 "Portuguese": "Reinício..."},
            "EJ":
                {"Spanish": f"Datos incompletos \n Ejemplo: {subs}",
                 "English": f"Incomplete data \n Example: {subs}",
                 "Portuguese": f"Dados incompletos \n Exemplo: {subs}"},
            "EX":
                {"Spanish": f"Ejemplo: {subs}",
                 "English": f"Example: {subs}",
                 "Portuguese": f"Exemplo: {subs}"},
            "Error Entering Client ID":
                {"Spanish": f"'{subs[0]}' no es válido. \n Ingresa números \n Ejemplo: {subs[1]}",
                 "English": f"'{subs[0]}' is invalid. \n Enter numbers \n Example: {subs[1]}",
                 "Portuguese": f"'{subs[0]}' é inválido. \n Digite os números \n Exemplo: {subs[1]}"},
            "Error Entering Player ID":
                {"Spanish": f"'{subs}' no es válido. \n Ingresa el ID del jugador. consulta el comando '-i'",
                 "English": f"'{subs}' no es válido. \n Add the player ID. use the '-i' command for more information.",
                 "Portuguese": f"'{subs}' no es válido. \n Adicione o ID do jogador. use o comando '-i' para obter mais informações."},
            "Happy":
                {"Spanish": "¡Estás felíz!",
                 "English": "Are you happy!",
                 "Portuguese": "Você está feliz!"},
            "Add Admin Msg":
                {"Spanish": f"'{subs}' Se agregó a la lista de Admins",
                 "English": f"'{subs}' Added to Admins list",
                 "Portuguese": f"'{subs}' Adicionado à lista de administradores"},
            "Delete Admin Msg":
                {"Spanish": f"Se removió a '{subs}' de la lista de Admins",
                 "English": f"'{subs}' was removed from the Admins list",
                 "Portuguese": f"'{subs}' foi removido da lista de administradores"},
            "Players Data":
                {"Spanish": "Nombre | Jugador ID | Cliente ID",
                 "English": "Name | Player ID | Client ID",
                 "Portuguese": "Nome |  Jogador ID |  ID do Cliente"},
            "Party Info":
                {"Spanish": f"{icons[0]}|Host: {subs[0]}\n{icons[1]}|Descripción: {subs[1]}\n{icons[1]}|Versión: {ba.app.version}",
                 "English": f"{icons[0]}|Host: {subs[0]}\n{icons[1]}|Description: {subs[1]}\n{icons[1]}|Version: {ba.app.version}",
                 "Portuguese": f"{icons[0]}|Host: {subs[0]}\n{icons[1]}|Descrição: {subs[1]}|\n{icons[1]}|Versão: {ba.app.version}"},
            "Same Player":
                  {"Spanish": "No puedes expulsarte a tí mismo",
                   "English": "You cannot expel yourself",
                   "Portuguese": "Você não pode se expulsar"},
            "Kick Msg":
                  {"Spanish": f"Sin rodeos, {subs[0]} ha expulsado a {subs[1]}",
                   "English": f"{subs[0]} kicked {subs[1]} Goodbye!",
                   "Portuguese": f"{subs[0]} expulsou {subs[1]}"},
            "User Invalid":
                {"Spanish": f"'{subs}' No le pertenece a ningún jugador.",
                 "English": f"'{subs}' Does not belong to any player.",
                 "Portuguese": f"'{subs}' Não pertence a nenhum jogador."},
            "Chat Live":
                {"Spanish": f"{icons[0]} CHAT EN VIVO {icons[0]}",
                 "English": f"{icons[0]} CHAT LIVE {icons[0]}",
                 "Portuguese": f"{icons[0]} BATE-PAPO AO VIVO {icons[0]}"},
            "Not Exists Node":
                {"Spanish": "No estás en el juego",
                 "English": "You're not in the game",
                 "Portuguese": "Você não está no jogo"},
            "Show Spaz Messages":
                {"Spanish": "Mostrar mensajes arriba de los jugadores.",
                 "English": "Show messages above players.",
                 "Portuguese": "Mostrar mensagens acima dos jogadores."},
            "Mute Message":
                {"Spanish": f"Se silenció a {subs}",
                 "English": f"{subs} was muted",
                 "Portuguese": f"{subs} foi silenciado"},
            "Unmute Message":
                {"Spanish": f"Se quitó el muteo a {subs}",
                 "English": f"{subs} can chat again",
                 "Portuguese": f"{subs} pode conversar novamente"},
            "Not In Admins":
                {"Spanish": f"No se puede silenciar a [{subs}] porque es administrador.",
                 "English": f"[{subs}] cannot be muted because he is an administrator.",
                 "Portuguese": f"[{subs}] não pode ser silenciado porque é um administrador."},
            "Module Not Found":
                {"Spanish": "No se encontraron los módulos. usa el comando '!dw' para descargarlos.",
                 "English": "Modules not found. use the '!dw' command to download them.",
                 "Portuguese": "Módulos não encontrados.  use o comando '!dw' para baixá-los."},
            "Clima Error Message":
                {"Spanish": "Selecciona un clima,\n Usa el comando '-climas' para más información.",
                 "English": "Select a weather,\n Use the command '-climas' for more information.",
                 "Portuguese": "Selecione um clima,\n Use o comando '-climas' para mais informações."},
            "Clima Message":
                {"Spanish": f"Se cambió el clima a '{subs}'",
                 "English": f"The weather is now '{subs}'",
                 "Portuguese": f"O tempo está agora '{subs}'"},
           "None Account":
                {"Spanish": "Información del jugador no válida.",
                 "English": "Informações do jogador inválidas.",
                 "Portuguese": "Informações do jogador inválidas."}, 
           "Error ID User":
                {"Spanish": f"Se produjo un error al ingresar el ID del jugador. \n '{subs}' no es válido.",
                 "English": f"An error occurred while entering the player ID. \n '{subs}' is not valid.",
                 "Portuguese": f"Ocorreu um erro ao inserir o ID do jogador.  \n '{subs}' não é válido."},
           "Effect Invalid":
                {"Spanish": f"'{subs}' es inválido. ingresa el comando '-effects' para más información.",
                 "English": f"'{subs}' is invalid. enter the command '-effects' for more information.",
                 "Portuguese": f"'{subs}' é inválido. digite o comando '-effects' para mais informações."},
           "Use -i Command":
                {"Spanish": "Le sugerimos usar el comando '-i'",
                 "English": "We suggest you use the '-i' command",
                 "Portuguese": "Sugerimos que você use o comando '-i'"},
           "Add Effect Message":
                {"Spanish": f"Se agregó el efecto '{subs[0]}' a {subs[1]}",
                 "English": f"Added '{subs[0]}' effect to {subs[1]}",
                 "Portuguese": f"Adicionado efeito '{subs[0]}' para {subs[1]}"},
           "You Are Amazing":
                {"Spanish": "¡¡Eres ASOMBROSO!!",
                 "English": "You Are Amazing!!",
                 "Portuguese": "Desculpe, o anfitrião é a autoridade máxima."},
           "Exe":
                {"Spanish": "Comando Ejecutado",
                 "English": "Command Executed",
                 "Portuguese": "Comando Executado"
            },
                 
            # ES
            "Agrega un texto":
                {"Spanish": "Añade un texto",
                 "English": "Add text",
                 "Portuguese": "Adicione texto"},
            "Cambios Guardados":
                {"Spanish": "Información guardada correctamente",
                 "English": "Information saved successfully",
                 "Portuguese": "Informações salvas com sucesso"},
            "Info Color":
                {"Spanish": "Argumento no válido, \n te sugerimos usar el comando '-colors'",
                 "English": "Invalid argument, \n we suggest you use the '-colors' command",
                 "Portuguese": "Argumento inválido, \n sugerimos que você use o comando '-colors'"},
            "ID Cliente Msj":
                {"Spanish": "Agrega el ID del cliente. \n utilice el comando '-i' para más información.",
                 "English": "Add the client ID.  \n use the '-i' command for more information.",
                 "Portuguese": "Adicione o ID do cliente. \n use o comando '-i' para mais informações."},
            "Guardando Informacion":
                {"Spanish": "Estamos guardando sus datos...",
                 "English": "Saving user data...",
                 "Portuguese": "Estamos salvando seus dados..."},
            "Ban A Admin Mensaje":
                {"Spanish": f"No puedes expulsar a [{subs}] porque es administrador",
                 "English": f"You can't kick [{subs}] because he's an admin",
                 "Portuguese": f"Você não pode chutar [{subs}] porque ele é um administrador"},
            "No Info Activa":
                {"Spanish": "Necesitas tener activa la información.\n Usa el comando '-info' para activarle.",
                 "English": "You need to have info active.\n Use the '-info' command to activate it",
                 "Portuguese": "Você precisa ter as informações ativas.\n Use o comando '-info' para ativá-las"},
                     }
    
        language = ["Spanish", "English", "Portuguese"]
        if lang not in language:
            lang = "English"
            
        if text not in setphrases:
            self.text = text
        else:
            self.text = setphrases[text][lang]
    
    def get(self):
        return self.text

def getlanguage(*args, **kwargs) -> str:
    subs = kwargs.get('subs', 'none')
    
    if type(subs) is not list:
        subs = str(subs)
    else:
        subs = [str(s) for s in subs]
    try:
        text = Lang(*args, subs=subs).get()
    except (IndexError, Exception):
        text = Lang(*args).get()
        text = text.replace('none', str(subs))
    finally:
        return text

calls: dict[str, Any] = {}
Chats: list[str] = []
roster = _ba.get_game_roster
act = _ba.get_foreground_host_activity
mutelist = list()

cfg = dict()

class PopupText(ptext.PopupText):
    """New PopupText.
    
    category: **Messages In Game**
    """
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.node.shadow = 10.0
        self.node.color = (1.5, 1.5, 1.5, 1.0)
        ba.animate(self._combine, 'input3', {0: 0, 0.1: 1.0})
        
    def handlemessage(self, msg: Any) -> Any | None:
        pass
    
class Commands:
    """Usa los distintos comandos dependiendo tu rango (All, Admins).
    
    Category: **Command Class**
    """

    fct: CommandFunctions
    "Llama los distintos comandos"
    
    util: Uts
    "Llama a las distintas utilidades"
    
    @property
    def get(self) -> str | None:
        return self.value
    
    def __init__(self,
                 msg: str,
                 client_id: int,
                 arguments: list[str] = []) -> None:
            
        self.message = msg
        self.msg = msg.strip()
        self.client_id = client_id
        self.arguments = arguments
        self.value = None

        self.util = Uts
        self.fct = CommandFunctions

        self.filter_chat()
        
    def clientmessage(self, msg: str,
            color: Sequence[float] | None = None):
                
        self.util.sm(msg, color=color,
            transient=True,
            clients=[self.client_id])
    
    def filter_chat(self) -> None:
        ms = self.arguments
        self.util.update_usernames()
                
        if self.client_id in self.util.accounts:
            if self.util.accounts[self.client_id]['Mute']:
                return setattr(self, 'value', '@')
        
        if cfg['Commands'].get('ShowMessages'):
            cls_node = self.fct.get_actor(self.client_id)
            if cls_node is not None:
                ActorMessage(self.msg, cls_node)
        
        if 'info' in ms[0].lower():
            with ba.Context(act()):
                ba.timer(0.01, ba.Call(self.util.create_data_text, act()))
                
        with ba.Context(act()):
            ba.timer(0.01, ba.Call(self.util.create_live_chat, act(),
                chat=[self.client_id, self.message],
                admin=self.fct.user_is_admin(self.client_id)))
    
        self.command_all()
        
        if self.fct.user_is_admin(self.client_id):
            self.admin_commands()
    
    def command_all(self) -> None:
        msg = self.msg.strip()
        ms = self.arguments
        cmd = self.fct.all_cmd()
        cls_node = self.fct.get_actor(self.client_id)
        ClientMessage = self.clientmessage
    
        if msg.lower() == cmd[0]: # -i
            self.fct.get_user_list(self.client_id)
    
        elif msg.lower() == cmd[1]: # -pan
            self.util.cm("¡Haz recibido pan de \ue061Sr.Palomo!")
            #return setattr(self, 'value', '@')
            
        elif msg.lower() == cmd[2]: # -ceb
            with ba.Context(act()):
                cls_node.handlemessage(
                    ba.CelebrateMessage(duration=3.0))
            ClientMessage(getlanguage('Happy'), color=(1.0, 1.0, 0.0))
            
        elif msg.lower() == cmd[3]: # -colors
            cols = str()
            cols_list = self.util.sort_list(self.util.colors())
            for c in cols_list:
                cols += (' | '.join(c) + '\n')
            ClientMessage(cols)
            
        elif msg.lower() == cmd[4]: # -mp (max players)
            mp = _ba.get_public_party_max_size()
            ClientMessage(ba.Lstr(value='${LSTR}: ${COUNT}',
                    subs=[('${LSTR}', ba.Lstr(resource='maxPartySizeText')),
                          ('${COUNT}', str(mp))]))

        elif msg.lower() == cmd[5]: # -pb
            self.fct.get_my_pb(self.client_id)
    
        elif msg.lower() == cmd[6]: # -effects
            cols = str()
            for e in self.fct.effects():
                cols += (' | ' + e)
            ClientMessage(cols)
    
    def admin_commands(self) -> None:
        msg = self.msg.strip()
        ms = self.arguments
        cls_node = self.fct.get_actor(self.client_id)
        ClientMessage = self.clientmessage

        ms[0] = ms[0].lower()
        cmd = [cd.lower() for cd in self.fct.admins_cmd()]
    
        if ms[0] == cmd[0]: # /name 0 La Pulga
            try: name = ms[2]
            except:
                color = self.util.colors()['orange']
                ClientMessage(getlanguage('EJ',
                    subs=ms[0] + ' 0  La Pulga | ' + ms[0] + ' all La Pulga'), color=color)
            else:
                self.fct.actor_command(ms=ms,
                    call=ba.Call(self.fct.actor_name, ' '.join(ms[2:])),
                    attrs={'Actor': cls_node,
                           'ClientMessage': ClientMessage})
    
        elif ms[0] == cmd[1]: # /imp
            self.fct.actor_command(ms=ms,
                call=self.fct.impulse,
                attrs={'Actor': cls_node,
                       'ClientMessage': ClientMessage})
            
        elif ms[0] == cmd[2]: # /box
            self.fct.actor_command(ms=ms,
                call=self.fct.spaz_box,
                attrs={'Actor': cls_node,
                       'ClientMessage': ClientMessage})
                       
        elif ms[0] == cmd[3] or ms[0] == cmd[4]: # /addAdmin
            if len(ms) == 1:
                ClientMessage(getlanguage('ID Cliente Msj'))
            else:
                try:
                    c_id = int(ms[1])
                except ValueError:
                    ClientMessage(
                            getlanguage('Error Entering Client ID',
                                subs=[ms[1], '/addAdmin 113']))
                else:
                    if c_id not in self.util.usernames:
                            ClientMessage(getlanguage('User Invalid', subs=c_id))
                    else:
                        if ms[0] == cmd[3]:
                            self.util.add_or_del_user(c_id, add=True)
                        else:
                            self.util.add_or_del_user(c_id, add=False)
                        
        elif ms[0] == cmd[5]: # /kill
            self.fct.actor_command(ms=ms,
                call=self.fct.kill_spaz,
                attrs={'Actor': cls_node,
                       'ClientMessage': ClientMessage})
                        
        elif ms[0] == cmd[6]: # -pause
            self.fct.pause()
                        
        elif ms[0] == cmd[7]: # /infoHost
            if not cfg['Commands'].get('ShowInfo'):
                ClientMessage(getlanguage('No Info Activa'))
            else:
                if len(ms) == 1:
                    ClientMessage(getlanguage('Agrega un texto'))
                else:
                    cfg['Commands']['HostName'] = ' '.join(ms[1:])
                    self.util.save_settings()
                    ClientMessage(getlanguage('Informacion guardada'), color=(0.0, 1.0, 0.0))
                
        elif ms[0] == cmd[8]: # /infoDes
            if not cfg['Commands'].get('ShowInfo'):
                ClientMessage(getlanguage('No Info Activa'))
            else:
                if len(ms) == 1:
                    ClientMessage(getlanguage('Agrega un texto'))
                else:
                    cfg['Commands']['Description'] = ' '.join(ms[1:])
                    self.util.save_settings()
                    ClientMessage(getlanguage('Informacion guardada'), color=(0.0, 1.0, 0.0))
    
        elif ms[0] == cmd[9]: # -info
            if cfg['Commands'].get('ShowInfo'):
                cfg['Commands']['ShowInfo'] = False
                color = self.util.colors()['red']
            else:
                cfg['Commands']['ShowInfo'] = True
                color = self.util.colors()['green']
                
            self.util.save_settings()
            ClientMessage(getlanguage('Cambios Guardados'), color=color)
    
        elif ms[0] == cmd[10]: # /infoColor
            if not cfg['Commands'].get('ShowInfo'):
                ClientMessage(getlanguage('No Info Activa'))
            else:
                if len(ms) == 1:
                    ClientMessage(getlanguage('Info Color'))
                else:
                    if ms[1] not in self.util.colors():
                        ClientMessage(getlanguage('Info Color'), color=(1, 0.5, 0))
                    else:
                        cfg['Commands']['InfoColor'] = self.util.colors()[ms[1]]
                        self.util.save_settings()
                        ClientMessage(getlanguage('Cambios Guardados'), color=(1, 1, 0))
    
        elif ms[0] == cmd[11]: # -end
            with ba.Context(act()):
                act().end_game()
    
        elif ms[0] == cmd[12]: # /kick
            if len(ms) == 1:
                ClientMessage(getlanguage('ID Cliente Msj'))
            else:
                try:
                    c_id = int(ms[1])
                except Exception as exc:
                    type_error = type(exc)
                    if type_error is ValueError:
                        ClientMessage(
                            getlanguage('Error Entering Client ID',
                                subs=[ms[1], ms[0] + ' 113']))
                    else:
                        ClientMessage(f'{type(e).__name__}: {e}')
                else:
                    if self.client_id == c_id:
                        ClientMessage(getlanguage('Same Player'))
                    else:
                        if c_id not in self.util.usernames:
                            ClientMessage(getlanguage('User Invalid', subs=c_id))
                        else:
                            user1 = self.util.usernames[self.client_id]
                            user2 = self.util.usernames[c_id]
                            if self.fct.user_is_admin(c_id):
                                ClientMessage(getlanguage('Ban A Admin Mensaje', subs=user2))
                            else:
                                self.util.cm(getlanguage('Kick Msg', subs=[user1, user2]))
                                _ba.disconnect_client(c_id)
    
        elif ms[0] == cmd[13]: # /-chatLive
            if cfg['Commands'].get('ChatLive'):
                cfg['Commands']['ChatLive'] = False
                color = self.util.colors()['red']
            else:
                cfg['Commands']['ChatLive'] = True
                color = self.util.colors()['green']
    
            self.util.save_settings()
            ClientMessage(getlanguage('Cambios Guardados'), color=color)
    
        elif ms[0] == cmd[14]: # /freeze
            self.fct.actor_command(ms=ms,
                call=self.fct.freeze_spaz,
                attrs={'Actor': cls_node,
                       'ClientMessage': ClientMessage})
            
        elif ms[0] == cmd[15]: # /playerColor
            try: color = ms[2]
            except IndexError:
                ClientMessage(getlanguage('Info Color'))
                ClientMessage(getlanguage('EJ',
                    subs=ms[0] + ' 0  yellow | ' + ms[0] + ' all green'))
            else:
                self.fct.actor_command(ms=ms,
                    call=ba.Call(self.fct.player_color, color),
                    attrs={'Actor': cls_node,
                           'ClientMessage': ClientMessage})
    
        elif ms[0] == cmd[16]: # /maxPlayers
            try:
                val = int(ms[1])
            except:
                ClientMessage(getlanguage('EJ', subs=ms[0] + ' 5'))
            else:
                _ba.set_public_party_max_size(val)
                ClientMessage(
                    ba.Lstr(value='${LSTR}: ${COUNT}',
                        subs=[('${LSTR}', ba.Lstr(resource='maxPartySizeText')),
                              ('${COUNT}', ms[1])]))
    
        elif ms[0] == cmd[17]: # -showMessages
            if cfg['Commands'].get('ShowMessages'):
                cfg['Commands']['ShowMessages'] = False
                color = self.util.colors()['red']
            else:
                cfg['Commands']['ShowMessages'] = True
                color = self.util.colors()['green']
    
            self.util.save_settings()
            ClientMessage(getlanguage('Show Spaz Messages'), color=color)
    
        elif ms[0] == cmd[18]: # /sleep
            self.fct.actor_command(ms=ms,
                call=self.fct.spaz_sleep,
                attrs={'Actor': cls_node,
                       'ClientMessage': ClientMessage})
    
        elif ms[0] == cmd[19] or ms[0] == cmd[20]: # /mute /unmute
            if len(ms) == 1:
                ClientMessage(getlanguage('ID Cliente Msj'))
            else:
                try:
                    c_id = int(ms[1])
                except Exception as e:
                    ClientMessage(
                        getlanguage('Error Entering Client ID',
                            subs=[ms[1], ms[0] + ' 113']))
                else:
                    if c_id not in self.util.accounts:
                        ClientMessage(getlanguage('User Invalid', subs=c_id))
                    else:
                        user = self.util.usernames[c_id]
                        if ms[0] == cmd[19]:
                            if self.fct.user_is_admin(c_id):
                                self.util.cm(getlanguage('Not In Admins', subs=Uts.usernames[c_id]))
                                return
                            if not self.util.accounts[c_id]['Mute']:
                                self.util.accounts[c_id]['Mute'] = True
                                self.util.cm(getlanguage('Mute Message', subs=user))
                        elif ms[0] == cmd[20]:
                            if self.util.accounts[c_id]['Mute']:
                                self.util.accounts[c_id]['Mute'] = False
                                self.util.cm(getlanguage('Unmute Message', subs=user))
                        Uts.save_players_data()

        elif ms[0] == cmd[21]: # /gm
            self.fct.actor_command(ms=ms,
                call=self.fct.spaz_gm,
                attrs={'Actor': cls_node,
                       'ClientMessage': ClientMessage})
    
        elif ms[0] == cmd[22]: # -slow
            self.fct.slow()

        elif ms[0] == cmd[23]: # /speed
            self.fct.actor_command(ms=ms,
                call=self.fct.spaz_speed,
                attrs={'Actor': cls_node,
                       'ClientMessage': ClientMessage})
                      
        elif ms[0] == cmd[24]: # /effect
            try:
                c_id = int(ms[1])
                eff = ms[2]
            except ValueError:
                ClientMessage(getlanguage('Error ID User', subs=ms[1]), color=(1, 0, 0))
            except IndexError:
                ClientMessage(getlanguage('ID Cliente Msj'), color=(1, 0.5, 0))
                ClientMessage(getlanguage('EJ', subs=ms[0] + ' 113 fire'), color=(1, 0.5, 0))
            else:
                if c_id not in self.util.accounts:
                    ClientMessage(getlanguage('User Invalid', subs=c_id), color=(1, 0.5, 0))
                    ClientMessage(getlanguage('Use -i Command'), color=(1, 0.5, 0))
                else:
                    if eff not in self.fct.effects():
                        ClientMessage(getlanguage('Effect Invalid', subs=eff), color=(1, 0.5, 0))
                    else:
                        self.util.accounts[c_id]['Effect'] = eff
                        self.util.save_players_data()
                        user = self.util.usernames[c_id]
                        ClientMessage(getlanguage('Add Effect Message',
                            subs=[eff, user]), color=(0, 0.5, 1))

        elif ms[0] == cmd[25]: # /punch
            self.fct.actor_command(ms=ms,
                call=self.fct.spaz_punch,
                attrs={'Actor': cls_node,
                       'ClientMessage': ClientMessage})
        
        elif ms[0] == cmd[26]: # /mbox
            self.fct.actor_command(ms=ms,
                call=self.fct.spaz_mgb,
                attrs={'Actor': cls_node,
                       'ClientMessage': ClientMessage})
                       
        elif ms[0] == cmd[27]: # /drop
            self.fct.actor_command(ms=ms,
                call=self.fct.spaz_drop,
                attrs={'Actor': cls_node,
                       'ClientMessage': ClientMessage})

        elif ms[0] == cmd[28]: # /gift
            self.fct.actor_command(ms=ms,
                call=self.fct.spaz_gift,
                attrs={'Actor': cls_node,
                       'ClientMessage': ClientMessage})
                       
        elif ms[0] == cmd[29]: # /curse
            self.fct.actor_command(ms=ms,
                call=self.fct.spaz_curse,
                attrs={'Actor': cls_node,
                       'ClientMessage': ClientMessage})
                       
        elif ms[0] == cmd[30]: # /superjump
            self.fct.actor_command(ms=ms,
                call=self.fct.spaz_sjump,
                attrs={'Actor': cls_node,
                       'ClientMessage': ClientMessage})
                       
class CommandFunctions:
    def all_cmd() -> list[str]:
        return [
            '-i', '-pan', '-ceb', '-colors',
            '-mp', '-pb', '-effects',
            ]
            
    def admins_cmd() -> list[str]:
        return [
            '-name', '-imp', '-box', '-addAdmin',
            '-delAdmin', '-kill', '-pause', '-infoHost',
            '-infoDes', '-info', '-infoColor', '-end',
            '-kick', '-chatLive', '-freeze', '-playerColor',
            '-maxPlayers', '-showMessages', '-sleep',
            '-mute', '-unmute', '-gm', '-slow', '-speed',
            '-effect', '-punch', '-mbox', '-drop', '-gift',
            '-curse', '-superjump',
            ]

    def effects() -> list[str]:
        return ['none', 'footprint', 'fire', 'darkmagic',
                'spark', 'stars', 'aure', 'chispitas', 'rainbow']

    def get_my_pb(client_id: int) -> None:
        print(Uts.userpbs)
        if Uts.userpbs.get(client_id):
            pb = Uts.userpbs[client_id]
            Uts.sm(pb, transient=True, clients=[client_id])
    
    def spaz_sjump(node: ba.Node) -> None:
        actor = node.source_player.actor
        del node # Unused by default.
        
        with ba.Context(act()):
            if getattr(actor, 'cm_superjump', None):
                actor.cm_superjump = False
            else:
                actor.cm_superjump = True
    
    def spaz_curse(node: ba.Node) -> None:
        with ba.Context(act()):
            node.handlemessage(ba.PowerupMessage('curse', node))
    
    def spaz_gift(node: ba.Node) -> None:
        with ba.Context(act()):
            ExplosiveGift(owner=node)
    
    def spaz_mgb(node: ba.Node) -> None:
        with ba.Context(act()):
            MagicBox(pos=node.position).autoretain()
            
    def spaz_punch(node: ba.Node) -> None:
        actor = node.source_player.actor
        del node # Unused by default.
        
        with ba.Context(act()):
            actor._punch_power_scale = 8.0
            
    def spaz_speed(node: ba.Node) -> None:
        with ba.Context(act()):
            if node.hockey:
                node.hockey = False
            else:
                node.hockey = True

    def slow() -> None:
        with ba.Context(act()):
            gnode = act().globalsnode
            if gnode.slow_motion:
                gnode.slow_motion = False
            else:
                gnode.slow_motion = True
            
    def spaz_gm(node: ba.Node) -> None:
        with ba.Context(act()):
            if node.invincible:
                node.invincible = False
            else:
                node.invincible = True
            
    def spaz_sleep(node: ba.Node) -> None:
        with ba.Context(act()):
            for x in range(5):
                ba.timer(x, ba.Call(node.handlemessage, 'knockout', 5000.0))
            
    def player_color(color: str, node: ba.Node) -> None:
        with ba.Context(act()):
            node.color = Uts.colors()[color]
            
    def freeze_spaz(node: ba.Node) -> None:
        actor = node.source_player.actor
        del node # Unused by default.
        
        with ba.Context(act()):
            if actor.shield:
                actor.shield.delete()
                
            actor.handlemessage(ba.FreezeMessage())

    def pause() -> None:
        with ba.Context(act()):
            globs = act().globalsnode
            if globs.paused:
                globs.paused = False
            else:
                globs.paused = True

    def kill_spaz(node: ba.Node) -> None:
        with ba.Context(act()):
            node.handlemessage(
                ba.DieMessage())

    def spaz_box(node: ba.Node) -> None:
        with ba.Context(act()):
            node.torso_model = ba.getmodel('tnt')
            node.head_model = None
            node.pelvis_model = None
            node.forearm_model = None
            node.color_texture = node.color_mask_texture = ba.gettexture('tnt')
            node.color = node.highlight = (1,1,1)
            node.style = 'cyborg'

    def impulse(node: ba.Node) -> None:
        msg = ba.HitMessage(pos=node.position,
                            velocity=node.velocity,
                            magnitude=500 * 4,
                            hit_type='imp',
                            radius=7840)
                          
        if isinstance(msg, ba.HitMessage):
            for i in range(2):
                with ba.Context(act()):
                    node.handlemessage(
                        'impulse', msg.pos[0], msg.pos[1], msg.pos[2],
                        msg.velocity[0], msg.velocity[1]+2.0, msg.velocity[2], msg.magnitude,
                        msg.velocity_magnitude, msg.radius, 0, msg.force_direction[0],
                        msg.force_direction[1], msg.force_direction[2])

    def actor_name(name: str, node: ba.Node) -> None:
        with ba.Context(act()):
            node.name = name

    def actor_command(
            ms: list[str],
            call: Callable,
            attrs: dict[str, Any]) -> None:
        ClientMessage = attrs['ClientMessage']
                
        def new_call(node: ba.Node):
            ClientMessage(getlanguage('Exe'), color=(0, 1, 0))
            call(node)
                
        if len(ms) == 1:
            if attrs['Actor'] is None:
                ClientMessage(getlanguage('Not Exists Node'))
            else:
                actor = attrs['Actor']
                new_call(actor.node)
        else:
            if ms[1] == 'all':
                for p in act().players:
                    node = p.actor.node
                    new_call(node)
            else:
                try:
                    p_id = int(ms[1])
                    node = act().players[p_id].actor.node
                except Exception as exc:
                    color = Uts.colors()['orange']
                    type_error = type(exc)
                    if type_error is ValueError:
                        ClientMessage(getlanguage('Error Entering Player ID', subs=ms[1]), color=color)
                    elif type_error is IndexError:
                        ClientMessage(getlanguage('User Invalid', subs=p_id), color=color)
                    else:
                        ClientMessage(f'{type(e).__name__}: {e}')
                    ClientMessage(getlanguage('EX', subs=ms[0] + ' 0 | ' + ms[0] + ' all'))
                else:
                    new_call(node)

    def spaz_drop(node: ba.Node) -> None:
        self = node.source_player.actor
        del node # Unused by default.

        def drop():
            pos = self.node.position
            psts = [
                (pos[0]-1,pos[1]+4,pos[2]+1),
                (pos[0]+1,pos[1]+4,pos[2]+1),
                (pos[0],pos[1]+4,pos[2]-1),
                (pos[0]-2,pos[1]+4,pos[2]),
                (pos[0]+2,pos[1]+4,pos[2]),
                (pos[0]+2,pos[1]+4,pos[2]-1),
                (pos[0]-2,pos[1]+4,pos[2]-1),
                (pos[0],pos[1]+4,pos[2]+2)]
                
            for p in psts:
                with ba.Context(act()):
                    bomb = Bomb(
                        position=p,
                        bomb_scale=1.3,
                        bomb_type='sticky').autoretain()
                    bomb.node.gravity_scale = 4.0
                    bomb.node.color_texture = ba.gettexture('bombStickyColor')
            
        for x in range(2):
            ba.timer(x * 0.308, ba.Call(drop))

    def get_user_list(c_id: int) -> None:
        def delete_text(t_id: int):
            if t_id == id(act()._ids.node):
                act()._ids.node.opacity = 0.0
            
        def gText(txt: str):
            act()._ids = text.Text(txt, position=(-0.0, 270.0),
                h_align=text.Text.HAlign.CENTER, scale=1.1,
                transition=text.Text.Transition.FADE_IN).autoretain()
            act()._ids.node.opacity = 0.5
            
            t_id = id(act()._ids.node)
            ba.timer(8.0, ba.Call(delete_text, t_id))
    
        txt = str()
        txts = [getlanguage('Players Data'),
                "______________________"]

        try:
            players = act().players
        except Exception:
            players = []
        else:
            for idx, p in enumerate(players):
                if p.is_alive():
                    s = p.sessionplayer
                    txts.append(f"{s.getname(False)} | {idx} | {s.inputdevice.client_id}")
        
        txt = '\n'.join(txts)

        with ba.Context(act()):
            try:
                if act()._ids.node.exists():
                    act()._ids.node.delete()
                    gText(txt)
            except AttributeError:
                gText(txt)
        ba.screenmessage(txt, clients=[c_id], transient=True)
    
    def get_characters() -> list[str]:
        return ba.app.spaz_appearances
    
    def user_is_admin(c_id: int) -> bool:
        if c_id == -1:
            return True
    
        if c_id in Uts.accounts:
            return Uts.accounts[c_id]['Admin']
        else:
            return False
    
    def get_actor(c_id: int) -> spaz.Spaz | None:
        act = _ba.get_foreground_host_activity()
        for player in act.players:
            if c_id == player.sessionplayer.inputdevice.client_id:
                return player.actor
        
def ActorMessage(msg: str, actor: spaz.Spaz):
    def die(node: ba.Node):
        if node.exists():
            ba.animate(popup.node, 'opacity', {0: 1.0, 0.1: 0.0})
            ba.timer(0.1, popup.node.delete)
        
    with ba.Context(act()):
        if getattr(actor, 'my_message', None):
            actor.my_message.node.delete()
        
        c = (1.0, 1.0, 1.0)
        position = (-0.0, 0.5, 0.0)

        m = ba.newnode('math', owner=actor.node, attrs={'input1':
            (position[0], position[1], position[2]), 'operation': 'add'})
        actor.node.connectattr('position_center', m, 'input2')
        
        actor.my_message = popup = PopupText(
             text=msg, color=c, scale=1.5).autoretain()
        m.connectattr('output', popup.node, 'position')
        ba.timer(5.0, ba.Call(die, popup.node))









# Effects
def _fire(self) -> None:
    if not self.node.exists():
        self._cm_effect_timer = None
    else:
        ba.emitfx(position=self.node.position,
        scale=3,count=50*2,spread=0.3,
        chunk_type='sweat')
    
def _spark(self) -> None:
    if not self.node.exists():
        self._cm_effect_timer = None
    else:
        ba.emitfx(position=self.node.position,
        scale=0.7,count=50*2,spread=0.3,
        chunk_type='spark')
    
def footprint(self) -> None:
    if not self.node.exists():
        self._cm_effect_timer = None
    else:
        loc = ba.newnode('locator', owner=self.node,
              attrs={
                     'position': self.node.position,
                     'shape': 'circle',
                     'color': self.node.color,
                     'size': [0.2],
                     'draw_beauty': False,
                     'additive': False})
        ba.animate(loc, 'opacity', {0: 1.0, 1.9: 0.0})
        ba.timer(2.0, loc.delete)
    
def aure(self) -> None:
    def anim(node: ba.Node) -> None:
        ba.animate_array(node, 'color', 3,
            {0: (1,1,0), 0.1: (0,1,0),
             0.2: (1,0,0), 0.3: (0,0.5,1),
             0.4: (1,0,1)}, loop=True)
        ba.animate_array(node, 'size', 1,
            {0: [1.0], 0.2: [1.5], 0.3: [1.0]}, loop=True)

    attrs = ['torso_position', 'position_center', 'position']
    for i, pos in enumerate(attrs):
        loc = ba.newnode('locator', owner=self.node,
              attrs={'shape': 'circleOutline',
                     'color': self.node.color,
                     'opacity': 1.0,
                     'draw_beauty': True,
                     'additive': False})
        self.node.connectattr(pos, loc, 'position')
        ba.timer(0.1 * i, ba.Call(anim, loc))
    
def stars(self) -> None:
    def die(node: ba.Node) -> None:
        if node:
            m = node.model_scale
            ba.animate(node, 'model_scale', {0: m, 0.1: 0})
            ba.timer(0.1, node.delete)
    
    if not self.node.exists() or self._dead:
        self._cm_effect_timer = None
    else:
        c = 0.3
        pos_list = [
            (c, 0, 0), (0, 0, c),
            (-c, 0, 0), (0, 0, -c)]
            
        for p in pos_list:
            m = 1.5
            np = self.node.position
            pos = (np[0]+p[0], np[1]+p[1]+0.0, np[2]+p[2])
            vel = (random.uniform(-m, m), random.uniform(2, 7), random.uniform(-m, m))

            texs = ['bombStickyColor', 'aliColor', 'aliColorMask', 'eggTex3']
            tex = ba.gettexture(random.choice(texs))
            model = ba.getmodel('flash')
            factory = SpazFactory.get()
            
            mat = ba.Material()
            mat.add_actions(
                conditions=('they_have_material', factory.punch_material),
                actions=(
                    ('modify_part_collision', 'collide', False),
                    ('modify_part_collision', 'physical', False),
                ))

            node = ba.newnode('prop',
                owner=self.node,
                attrs={'body': 'sphere',
                       'position': pos,
                       'velocity': vel,
                       'model': model,
                       'model_scale': 0.1,
                       'body_scale': 0.0,
                       'shadow_size': 0.0,
                       'gravity_scale': 0.5,
                       'color_texture': tex,
                       'reflection': 'soft',
                       'reflection_scale': [1.5],
                       'materials': [mat]})
            
            light = ba.newnode('light',
                owner=node,
                attrs={
                    'intensity': 0.3,
                    'volume_intensity_scale': 0.5,
                    'color': (random.uniform(0.5, 1.5),
                              random.uniform(0.5, 1.5),
                              random.uniform(0.5, 1.5)),
                    'radius': 0.035})
            node.connectattr('position', light, 'position')
            ba.timer(0.25, ba.Call(die, node))
            
def chispitas(self) -> None:
    def die(node: ba.Node) -> None:
        if node:
            m = node.model_scale
            ba.animate(node, 'model_scale', {0: m, 0.1: 0})
            ba.timer(0.1, node.delete)
    
    if not self.node.exists() or self._dead:
        self._cm_effect_timer = None
    else:
        c = 0.3
        pos_list = [
            (c, 0, 0), (0, 0, c),
            (-c, 0, 0), (0, 0, -c)]
            
        for p in pos_list:
            m = 1.5
            np = self.node.position
            pos = (np[0]+p[0], np[1]+p[1]+0.0, np[2]+p[2])
            vel = (random.uniform(-m, m), random.uniform(2, 7), random.uniform(-m, m))

            tex = ba.gettexture('null')
            model = None
            factory = SpazFactory.get()
            
            mat = ba.Material()
            mat.add_actions(
                conditions=('they_have_material', factory.punch_material),
                actions=(
                    ('modify_part_collision', 'collide', False),
                    ('modify_part_collision', 'physical', False),
                ))

            node = ba.newnode('bomb',
                owner=self.node,
                attrs={'body': 'sphere',
                       'position': pos,
                       'velocity': vel,
                       'model': model,
                       'model_scale': 0.1,
                       'body_scale': 0.0,
                       'color_texture': tex,
                       'fuse_length': 0.1,
                       'materials': [mat]})
            
            light = ba.newnode('light',
                owner=node,
                attrs={
                    'intensity': 0.3,
                    'volume_intensity_scale': 0.5,
                    'color': (random.uniform(0.5, 1.5),
                              random.uniform(0.5, 1.5),
                              random.uniform(0.5, 1.5)),
                    'radius': 0.035})
            node.connectattr('position', light, 'position')
            ba.timer(0.25, ba.Call(die, node))
            
def darkmagic(self) -> None:
    def die(node: ba.Node) -> None:
        if node:
            m = node.model_scale
            ba.animate(node, 'model_scale', {0: m, 0.1: 0})
            ba.timer(0.1, node.delete)
    
    if not self.node.exists() or self._dead:
        self._cm_effect_timer = None
    else:
        c = 0.3
        pos_list = [
            (c, 0, 0), (0, 0, c),
            (-c, 0, 0), (0, 0, -c)]
            
        for p in pos_list:
            m = 1.5
            np = self.node.position
            pos = (np[0]+p[0], np[1]+p[1]+0.0, np[2]+p[2])
            vel = (random.uniform(-m, m), 30.0, random.uniform(-m, m))

            tex = ba.gettexture('impactBombColor')
            model = ba.getmodel('impactBomb')
            factory = SpazFactory.get()
            
            mat = ba.Material()
            mat.add_actions(
                conditions=('they_have_material', factory.punch_material),
                actions=(
                    ('modify_part_collision', 'collide', False),
                    ('modify_part_collision', 'physical', False),
                ))

            node = ba.newnode('prop',
                owner=self.node,
                attrs={'body': 'sphere',
                       'position': pos,
                       'velocity': vel,
                       'model': model,
                       'model_scale': 0.4,
                       'body_scale': 0.0,
                       'shadow_size': 0.0,
                       'gravity_scale': 0.5,
                       'color_texture': tex,
                       'reflection': 'soft',
                       'reflection_scale': [0.0],
                       'materials': [mat]})
            
            light = ba.newnode('light',
                owner=node,
                attrs={'intensity': 1.0,
                       'volume_intensity_scale': 0.5,
                       'color': (0.5, 0.0, 1.0),
                       'radius': 0.035})
            node.connectattr('position', light, 'position')
            ba.timer(0.25, ba.Call(die, node))
            
def _rainbow(self) -> None:
    keys = {
        0.0: (2.0, 0.0, 0.0),
        0.2: (2.0, 1.5, 0.5),
        0.4: (2.0, 2.0, 0.0),
        0.6: (0.0, 2.0, 0.0),
        0.8: (0.0, 2.0, 2.0),
        1.0: (0.0, 0.0, 2.0),
    }.items()

    def _changecolor(color: Sequence[float]) -> None:
        if self.node.exists():
            self.node.color = color

    for time, color in keys:
        ba.timer(time, ba.Call(_changecolor, color))
           
def apply_effect(self, eff: str | None) -> None:
    if eff == 'fire':
        call = ba.Call(_fire, self)
        self._cm_effect_timer = ba.Timer(0.1, call, repeat=True)
    elif eff == 'spark':
        call = ba.Call(_spark, self)
        self._cm_effect_timer = ba.Timer(0.1, call, repeat=True)
    elif eff == 'footprint':
        call = ba.Call(footprint, self)
        self._cm_effect_timer = ba.Timer(0.15, call, repeat=True)
    elif eff == 'stars':
        call = ba.Call(stars, self)
        self._cm_effect_timer = ba.Timer(0.1, call, repeat=True)
    elif eff == 'chispitas':
        call = ba.Call(chispitas, self)
        self._cm_effect_timer = ba.Timer(0.1, call, repeat=True)
    elif eff == 'darkmagic':
        call = ba.Call(darkmagic, self)
        self._cm_effect_timer = ba.Timer(0.1, call, repeat=True)
    elif eff == 'rainbow':
        call = ba.Call(_rainbow, self)
        self._cm_effect_timer = ba.Timer(1.2, call, repeat=True)
    elif eff == 'aure':
        aure(self)
    
# -----------

def filter_chat_message(msg: str, client_id: int) -> None:
    command = Commands(msg, client_id, msg.split(' '))
    return command.get
    
def new_ga_on_transition_in(self) -> None:
    calls['GA_OnTransitionIn'](self)
    _ba.set_party_icon_always_visible(True)
    Uts.create_data_text(self)
    Uts.create_live_chat(self, live=False)

def new_on_player_join(self, player: ba.Player) -> None:
    calls['OnPlayerJoin'](self, player)
    Uts.player_join(player)
    
def new_playerspaz_init_(self, *args, **kwargs) -> None:
    calls['PlayerSpazInit'](self, *args, **kwargs)
    Uts.update_usernames()

    user = self._player.sessionplayer.get_v1_account_id()
    if user in Uts.pdata:
        eff = Uts.pdata[user]['Effect']
        apply_effect(self, eff)
            
def new_playerspaz_on_jump_press(self) -> None:    
    calls['OnJumpPress'](self)
    
    if not getattr(self, 'cm_superjump', False):
        return
        
    if (not self.node or not self.node.jump_pressed):
        return
    
    msg = ba.HitMessage(pos=self.node.position,
                        velocity=self.node.velocity,
                        magnitude=160*2,
                        hit_type='imp',
                        radius=460*2)
                      
    if isinstance(msg, ba.HitMessage):
        for i in range(2):
            with ba.Context(act()):
                self.node.handlemessage(
                    'impulse', msg.pos[0], msg.pos[1], msg.pos[2],
                    msg.velocity[0], msg.velocity[1]+2.0, msg.velocity[2], msg.magnitude,
                    msg.velocity_magnitude, msg.radius, 0, msg.force_direction[0],
                    msg.force_direction[1], msg.force_direction[2])
            
# -----------

class ExplosiveGift(ba.Actor):
    def __init__(self,
                 time: float = 3.0,
                 owner: ba.Node = None):
        super().__init__()
        
        self.time = time
        self.owner = owner
        self.scale = 0.8
        self.touch = False
        
        pos = list(owner.position)
        velocity = (0.0, 60, 0.0)
        position = (pos[0], pos[1]+1.47, pos[2])
                     
        tex = ba.gettexture('crossOutMask')
        model = ba.getmodel('tnt')
                     
        self.node = ba.newnode('bomb',
                               delegate=self,
                               attrs={'body': 'sphere',
                                      'position': position,
                                      'velocity': velocity,
                                      'model': model,
                                      'body_scale': self.scale,
                                      'shadow_size': 0.3,
                                      'color_texture': tex,
                                      'sticky': True,
                                      'owner': owner,
                                      'reflection': 'soft',
                                      'reflection_scale': [0.22]})
        ba.animate(self.node, 'model_scale',
           {0: 0,
            0.2: self.scale * 1.3,
            0.26: self.scale})
        ba.animate(self.node, 'fuse_length', {0.0: 1.0, time: 0.0})
        ba.timer(time, self._xplosion)
        
    def _xplosion(self):
        radius = 3.0
        shared = SharedObjects.get()
        
        mat = ba.Material()
        mat.add_actions(
            conditions=(
                ('they_have_material', shared.player_material), 'or',
                ('they_have_material', shared.object_material)
            ),
            actions=(
                ('modify_part_collision', 'collide', True),
                ('modify_part_collision', 'physical', False),
                ('call', 'at_connect', self.call)
            ))
        
        rmats = [mat, shared.attack_material]

        region = ba.newnode('region',
            delegate=self,
            owner=self.node,
            attrs={'scale': tuple(radius*0.7 for s in range(3)),
                   'type': 'sphere',
                   'materials': rmats})
        self.node.connectattr('position', region, 'position')
        
        shield = ba.newnode('shield',
            owner=region,
                attrs={'color': (2.0, 1.0, 0.0),
                       'radius': radius})
        region.connectattr('position', shield, 'position')
        
        ba.playsound(ba.getsound('explosion03'), 1, self.node.position)
        ba.timer(0.1, ba.Call(
            self.handlemessage, ba.DieMessage()))
        
    def call(self) -> None:
        node = ba.getcollision().opposingnode
        
        def action():
            #if node != self.owner or node != self.node:
                msg = ba.HitMessage(
                    pos=self.node.position,
                    velocity=node.velocity,
                    magnitude=1200 * 5,
                    radius=800 * 5)

                node.handlemessage(
                    'impulse', msg.pos[0], msg.pos[1], msg.pos[2],
                    msg.velocity[0], msg.velocity[1]+2.0, msg.velocity[2], msg.magnitude,
                    msg.velocity_magnitude, msg.radius, 0, msg.force_direction[0],
                    msg.force_direction[1], msg.force_direction[2])

        if not self.touch:
            self.touch = True
        else:
            action()
            self.touch = False
        
    def handlemessage(self, msg: Any) -> Any:
        if isinstance(msg, ba.DieMessage):
            if self.node:
                self.node.delete()
        else:
            return super().handlemessage(msg)

class MagicBox(ba.Actor):
    def __init__(self, pos: Sequence[float] = (0.0, 1.0, 0.0)) -> None:
        super().__init__()
        
        shared = SharedObjects.get()
        tex = ba.gettexture('rgbStripes')
        model = ba.getmodel('powerup')
        position = (pos[0], pos[1] + 1.5, pos[2])
        
        self.node = ba.newnode('prop',
            delegate=self,
            attrs={'body': 'box',
                   'position': position,
                   'model': model,
                   'shadow_size': 0.5,
                   'color_texture': tex,
                   'reflection': 'powerup',
                   'reflection_scale': [1.0],
                   'materials': [shared.object_material]})
        
    def handlemessage(self, msg: Any) -> Any:
        if isinstance(msg, ba.PickedUpMessage):
            self.node.gravity_scale = -1.0
        elif isinstance(msg, ba.DroppedMessage):
            self.node.gravity_scale = 1.0
        elif isinstance(msg, ba.DieMessage):
            if self.node:
                self.node.delete()
        else:
            return super().handlemessage(msg)



class Uts:
    directory_user: str = ba.app.python_directory_user
    directory_sys: str = directory_user + '/sys/' + ba.app.version
    sm: Callable = _ba.screenmessage
    cm: Callable = _ba.chatmessage
    key: str = '#CheatMax'
    mod: Any | None
    accounts: dict[int, Any] = {}
    usernames: dict[int, str] = {}
    shortnames: dict[int, str] = {}
    useraccounts: dict[int, str] = {}
    userpbs: dict[int, str] = {}
    players: dict[int, ba.SessionPlayer] = {}

    def get_user_name(c_id: int) -> str:
        for r in roster():
            if r['client_id'] == c_id:
                if r['players'] == []:
                    return r['display_string']
                else:
                    return r['players'][0]['name_full']
            break
        return 'UNNAMED'

    def sort_list(vals: list, count: int = 3) -> list:
        vals_dict = dict(r=[])
        
        for n in range(len(vals)):
            vals_dict[n] = list()
            
            for c in vals:
                if len(vals_dict[n]) == count:
                    break
                else:
                    if c not in vals_dict['r']:
                        vals_dict['r'].append(c)
                        vals_dict[n].append(c)
        
            if len(vals_dict['r']) == len(vals):
                vals_dict.pop('r')
                break

        return list(vals_dict.values())

    def colors() -> dict[str, Sequence[float]]:
        return dict(
                yellow=(1.0, 1.0, 0.0),
                red=(1.0, 0.0, 0.0),
                green=(0.0, 1.0, 0.0),
                blue=(0.2, 1.0, 1.0),
                pink=(1, 0.3, 0.5),
                orange=(1.0, 0.5, 0.0),
                violet=(0.5, 0.25, 1.0),
                white=(1.0, 1.0, 1.0),
                black=(0.25, 0.25, 0.25))

    def get_admins() -> list[str]:
        admins = []
        if len(Uts.pdata) > 0:
            for p, d in Uts.pdata.items():
                if d['Admin']:
                    admins.append(p)
        return admins

    def add_or_del_user(c_id: int, add: bool = True) -> None:
        if c_id == -1:
            return Uts.sm(getlanguage('You Are Amazing', subs=c_id), color=(0.5, 0, 1), clients=[c_id], transient=True)
            
        if c_id not in Uts.userpbs:
            Uts.sm(getlanguage('User Invalid', subs=c_id), clients=[c_id], transient=True)
        else:
            user = Uts.userpbs[c_id]
            if add:
                if user in Uts.pdata:
                    if not Uts.pdata[user]['Admin']:
                        Uts.pdata[user]['Admin'] = add
                        Uts.cm(getlanguage('Add Admin Msg', subs=Uts.usernames[c_id]))
            else:
                if user in Uts.pdata:
                    if Uts.pdata[user]['Admin']:
                        Uts.pdata[user]['Admin'] = add
                        Uts.cm(getlanguage('Delete Admin Msg', subs=Uts.usernames[c_id]))
            Uts.save_players_data()

    def create_players_data() -> None:
        folder = Uts.directory_user + '/Configs'
        file = folder + '/CheatMaxPlayersData.json'
                
        if not os.path.exists(folder):
            os.mkdir(folder)
            
        if not os.path.exists(file):
            with open(file, 'w') as f:
                f.write('{}')

        with open(file) as f:
            r = f.read()
            Uts.pdata = json.loads(r)

    def save_players_data() -> None:
        folder = Uts.directory_user + '/Configs'
        file = folder + '/CheatMaxPlayersData.json'
        with open(file, 'w') as f:
            w = json.dumps(Uts.pdata, indent=4)
            f.write(w)

    def player_join(player: ba.Player) -> None:
        try:
            sessionplayer = player.sessionplayer
            account_id = sessionplayer.get_v1_account_id()
            client_id = sessionplayer.inputdevice.client_id
            account_name = sessionplayer.inputdevice.get_v1_account_name(True)
        except Exception:
            account_id = None
        else:
            if type(account_id) is str and account_id.startswith('pb'):
                if account_id not in Uts.pdata:
                    Uts.add_player_data(account_id)
                    Uts.sm(getlanguage('Guardando Informacion'), color=(0.35, 0.7, 0.1), transient=True, clients=[client_id])
                    
                accounts = Uts.pdata[account_id]['Accounts']
                if account_name not in accounts:
                    accounts.append(account_name)
                    Uts.save_players_data()
                        
                Uts.accounts[client_id] = Uts.pdata[account_id]
            Uts.usernames[client_id] = account_name
            Uts.useraccounts[client_id] = account_name
            Uts.players[client_id] = sessionplayer
                
    def update_usernames() -> None:
        for r in roster():
            c_id = r['client_id']
            if c_id not in Uts.accounts:
                if r['account_id'] in Uts.pdata:
                    Uts.accounts[c_id] = Uts.pdata[r['account_id']]
            if c_id not in Uts.usernames:
                Uts.usernames[c_id] = r['display_string']
                
            acc = r['display_string']
            for acc_id, dt in Uts.pdata.items():
                for ac in dt['Accounts']:
                    if ac == acc:
                        Uts.accounts[c_id] = Uts.pdata[acc_id]
                        Uts.userpbs[c_id] = acc_id
                        
        for c_id, p in Uts.players.items():
            if p.exists():
                Uts.usernames[c_id] = p.getname(full=True)
                Uts.shortnames[c_id] = p.getname(full=False)
                
                if p.get_v1_account_id() is not None:
                    Uts.userpbs[c_id] = p.get_v1_account_id()
            
    def add_player_data(account_id: str) -> None:
        if account_id not in Uts.pdata:
            Uts.pdata[account_id] = {
                'Mute': False,
                'Effect': 'none',
                'Admin': False,
                'Accounts': []}
            Uts.save_players_data()

    def save_settings() -> None:
        global cfg
        folder = Uts.directory_user + '/Configs'
        file = folder + '/CheatMaxSettings.json'
        
        with open(file, 'w') as f:
            w = json.dumps(cfg, indent=4)
            f.write(w)

    def create_settings() -> None:
        global cfg
        folder = Uts.directory_user + '/Configs'
        file = folder + '/CheatMaxSettings.json'
        
        if not os.path.exists(folder):
            os.mkdir(folder)
        
        if not os.path.exists(file):
            with open(file, 'w') as f:
                f.write('{}')

        with open(file) as f:
            r = f.read()
            cfg = json.loads(r)

    def create_user_system_scripts() -> None:
        """Set up a copy of Ballistica system scripts under your user scripts dir.

        (for editing and experiment with)
        """
        import shutil
        app = _ba.app

        path = (app.python_directory_user + '/sys/' + app.version)
        pathtmp = path
        if os.path.exists(path):
            shutil.rmtree(path)
        if os.path.exists(pathtmp):
            shutil.rmtree(pathtmp)
    
        def _ignore_filter(src: str, names: Sequence[str]) -> Sequence[str]:
            del src, names  # Unused
    
            # We simply skip all __pycache__ directories. (the user would have
            # to blow them away anyway to make changes;
            # See https://github.com/efroemling/ballistica/wiki
            # /Knowledge-Nuggets#python-cache-files-gotcha
            return ('__pycache__', )
    
        print(f'COPYING "{app.python_directory_app}" -> "{pathtmp}".')
        shutil.copytree(app.python_directory_app, pathtmp, ignore=_ignore_filter)
    
        print(f'MOVING "{pathtmp}" -> "{path}".')
        shutil.move(pathtmp, path)
        print(f"Created system scripts at :'{path}"
              f"'\nRestart {_ba.appname()} to use them."
              f' (use ba.quit() to exit the game)')
        if app.platform == 'android':
            print('Note: the new files may not be visible via '
                  'android-file-transfer until you restart your device.')
        
    def create_data_text(self) -> None:
        if isinstance(act(), MainMenuActivity):
            return

        if getattr(self, '_text_data', None):
            self._text_data.node.delete()

        if cfg['Commands'].get('ShowInfo'):
            info = getlanguage('Party Info', subs=[
                cfg['Commands'].get('HostName', '???'),
                cfg['Commands'].get('Description', '???')])
            color = tuple(list(cfg['Commands'].get('InfoColor', Uts.colors()['white'])) + [1])
                
            self._text_data = text.Text(info,
                position=(-730.0, -200.0), scale=0.7, color=color)

    def create_live_chat(self,
                         live: bool = True,
                         chat: list[int, str] | None = None,
                         admin: bool = False) -> None:
        if isinstance(act(), MainMenuActivity):
            return
        
        if getattr(self, '_live_chat', None):
            self._live_chat.node.delete()
            
        if cfg['Commands'].get('ChatLive'):
            max = 6
            chats = list()
            txt = str()
            icon = ba.charstr(ba.SpecialChar.STEAM_LOGO) if admin else ''
            
            if any(_ba.get_chat_messages()):
                if len(Chats) == max:
                    Chats.pop(0)
                    
                if live:
                    name = Uts.shortnames.get(chat[0], chat[0])
                    msg = chat[1]
                    Chats.append(f'{icon}{name}: {msg}')
                
                for msg in Chats:
                    if len(chats) != max:
                        chats.append(msg)
                    else: break
                txt = '\n'.join(chats)
            
            livetext = getlanguage('Chat Live')
            txt = (livetext + '\n' + ''.join(['=' for s 
                in range(len(livetext))]) + '\n') + txt

            self._live_chat = text.Text(txt, position=(-734.0, 150.0),
                color=(1, 1, 1, 1), scale=0.7, h_align=text.Text.HAlign.LEFT)

    def funtion() -> str:
        return """    %s
    try:
        cm = _ba.app.cheatmax_filter_chat(msg, client_id)
        if cm == '@':
            return None
    except Exception:
        pass
        """ % Uts.key








def _install() -> None:
    from ba import modutils, _hooks, _app
    _file = Uts.directory_sys + '/ba/_hooks.py'
    ba.app.cheatmax_filter_chat = filter_chat_message

    def seq():
        Uts.sm(getlanguage('Installing'))

        ba.timer(2.0, ba.Call(
            Uts.sm, getlanguage('Installed'), (0.0, 1.0, 0.0)))
        
        ba.timer(4.0, ba.Call(
            Uts.sm, getlanguage('Restart Msg')))
        
        ba.timer(6.0, _ba.quit)
    
    if not os.path.exists(Uts.directory_sys):
        Uts.create_user_system_scripts()
        ba.timer(1.0, ba.Call(
            Uts.sm, getlanguage('Make Sys'), (0.0, 1.0, 0.0)))
        seq()
        del seq

    with open(_file) as s:
        read = s.read()
        read_l = read.split('\n')
        
    if Uts.key not in read:
        f_list = Uts.funtion().split('\n')
        ix = read_l.index('def filter_chat_message(msg: str, client_id: int) -> str | None:')
        
        for i, lt in enumerate(f_list):
            read_l.insert(i+(ix+1), lt)

        read = '\n'.join(read_l)
        with open(_file, 'w') as s:
            s.write(read)
        seq()

    Uts.create_players_data()
    #Uts.add_admin('pb-IF4XLRUN')
    Uts.save_players_data()

def settings():
    global cfg
    Uts.create_settings()
    
    if cfg.get('Commands') is None:
        cfg['Commands'] = dict()
        Uts.save_settings()
 
def plugin():
    calls['GA_OnTransitionIn'] = ba.GameActivity.on_transition_in
    calls['OnJumpPress'] = PlayerSpaz.on_jump_press
    calls['OnPlayerJoin'] = Activity.on_player_join
    calls['PlayerSpazInit'] = PlayerSpaz.__init__

    
    ba.GameActivity.on_transition_in = new_ga_on_transition_in
    PlayerSpaz.on_jump_press = new_playerspaz_on_jump_press
    Activity.on_player_join = new_on_player_join
    PlayerSpaz.__init__ = new_playerspaz_init_

# ba_meta export plugin
class Install(ba.Plugin):
    def __init__(self):
        plugin()
        settings()
        ba.timer(1.3, _install)
