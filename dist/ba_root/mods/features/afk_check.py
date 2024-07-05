import time
import ba
from ba._general import Call
import _ba
import ba.internal
import setting

settings = setting.get_settings_data()
INGAME_TIME = settings["afk_remover"]["ingame_idle_time_in_secs"]
LOBBY_KICK = settings['afk_remover']["kick_idle_from_lobby"]
INLOBBY_TIME = settings['afk_remover']["lobby_idle_time_in_secs"]

class CheckIdle:
    def __init__(self):
        self.t1 = ba.timer(2, ba.Call(self.check), repeat=True)
        self.lobbies = {}

    def check(self):
        current = ba.time(ba.TimeType.REAL, timeformat=ba.TimeFormat.MILLISECONDS)
        session = ba.internal.get_foreground_host_session()

        if not session:
            return

        self.check_ingame_idle(current, session)
        if LOBBY_KICK:
            self.check_lobby_idle(current)

    def check_ingame_idle(self, current, session):
        for player in session.sessionplayers:
            last_input = int(player.inputdevice.get_last_input_time())
            afk_time = int((current - last_input) / 1000)

            if INGAME_TIME <= afk_time <= INGAME_TIME + 20:
                remaining_time = INGAME_TIME + 20 - afk_time
                self.warn_player(player.get_v1_account_id(), f"Press any button within {remaining_time} secs")
            elif afk_time > INGAME_TIME + 20:
                player.remove_from_game()

    def check_lobby_idle(self, current):
        current_players = []
        for player in ba.internal.get_game_roster():
            if player['client_id'] != -1 and len(player['players']) == 0:
                client_id = player['client_id']
                current_players.append(client_id)
                if client_id not in self.lobbies:
                    self.lobbies[client_id] = current
                lobby_afk = int((current - self.lobbies[client_id]) / 1000)
                if INLOBBY_TIME <= lobby_afk <= INLOBBY_TIME + 10:
                    _ba.screenmessage(f"Join game within {10 - (lobby_afk - INLOBBY_TIME)} secs", color=(1, 0, 0), transient=True, clients=[client_id])
                elif lobby_afk > INLOBBY_TIME + 10:
                    ba.internal.disconnect_client(client_id, 0)

        self.lobbies = {clid: self.lobbies[clid] for clid in self.lobbies if clid in current_players}

    def warn_player(self, pbid, msg):
        for player in ba.internal.get_game_roster():
            if player["account_id"] == pbid:
                _ba.screenmessage(msg, color=(1, 0, 0), transient=True, clients=[player['client_id']])