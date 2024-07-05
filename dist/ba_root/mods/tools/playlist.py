# ba_meta require api 7

# Thanks to Rikko for playlist fetch by code

import ba
import _ba
import ba.internal
# session change by smoothy
from ba._freeforallsession import FreeForAllSession
from ba._dualteamsession import DualTeamSession
from ba._coopsession import CoopSession

import time
import _thread
import setting
from ba._general import Call
settings = setting.get_settings_data()

_ba.app.coop_session_args['max_players'] = 14
_ba.app.coop_session_args['campaign'] = "Default"
_ba.app.coop_session_args['level'] = "Onslaught Training"

def set_playlist(content):
    try:
        if content is None:
            return
        _playlists_var = "{} Playlists".format(content["playlistType"])
        playlists = _ba.app.config[_playlists_var]
        playlist = playlists[content["playlistName"]]
        ba.internal.chatmessage("Fetched playlist:" + content["playlistName"])
        typename = (
            'teams' if content['playlistType'] == 'Team Tournament' else
            'ffa' if content['playlistType'] == 'Free-for-All' else '??')
        return set_playlist_inline(playlist, typename)
    except Exception as e:
        error_message = f"Error in set_playlist: {e}"        
        print(error_message)

def set_playlist_inline(playlist, newPLaylistType):
    try:
        session = ba.internal.get_foreground_host_session()

        if (isinstance(session, DualTeamSession) or isinstance(session, CoopSession)) and newPLaylistType == 'ffa':
            ba.internal.get_foreground_host_session().end()
            _thread.start_new_thread(withDelay, (FreeForAllSession, playlist,))
        elif (isinstance(session, FreeForAllSession) or isinstance(session, CoopSession)) and newPLaylistType == "teams":
            ba.internal.get_foreground_host_session().end()
            _thread.start_new_thread(withDelay, (DualTeamSession, playlist,))
        else:
            updatePlaylist(playlist)
    except Exception as e:
        error_message = f"Error in set_playlist_inline: {e}"        
        print(error_message)

def withDelay(session, playlist):
    try:
        time.sleep(1)
        _ba.pushcall(Call(updateSession, session, playlist), from_other_thread=True)
    except Exception as e:
        error_message = f"Error in withDelay: {e}"        
        print(error_message)

def updateSession(session, playlist):
    try:
        ba.internal.new_host_session(session)
        if playlist:
            updatePlaylist(playlist)
    except Exception as e:
        error_message = f"Error in updateSession: {e}"        
        print(error_message)

def updatePlaylist(playlist):
    try:
        session = ba.internal.get_foreground_host_session()
        content = ba._playlist.filter_playlist(
            playlist,
            sessiontype=type(session),
            add_resolved_type=True,
        )
        playlist = ba._multiteamsession.ShuffleList(content, shuffle=False)
        session._playlist = playlist
        set_next_map(session, playlist.pull_next())
    except Exception as e:
        error_message = f"Error in updatePlaylist: {e}"        
        print(error_message)

def set_next_map(session, game_map):
    try:
        session._next_game_spec = game_map
        with ba.Context(session):
            session._instantiate_next_game()
    except Exception as e:
        error_message = f"Error in set_next_map: {e}"        
        print(error_message)

def playlist(code):
    try:
        ba.internal.add_transaction(
            {
                'type': 'IMPORT_PLAYLIST',
                'code': str(code),
                'overwrite': True
            },
            callback=set_playlist)
        ba.internal.run_transactions()
    except Exception as e:
        error_message = f"Error in playlist: {e}"        
        print(error_message)

def setPlaylist(para):
    try:
        if para.isdigit():
            playlist(para)
        elif para == "coop":
            _thread.start_new_thread(withDelay, (CoopSession, None,))
        elif para in settings["playlists"]:
            playlist(settings["playlists"][para])
        else:
            ba.internal.chatmessage("Available Playlist")
            for play in settings["playlists"]:
                ba.internal.chatmessage(play)
    except Exception as e:
        error_message = f"Error in setPlaylist: {e}"        
        print(error_message)

def flush_playlists():
    try:
        print("Clearing old playlists..")
        for playlist in _ba.app.config["Team Tournament Playlists"]:
            ba.internal.add_transaction(
                {
                    "type": "REMOVE_PLAYLIST",
                    "playlistType": "Team Tournament",
                    "playlistName": playlist
                })
        ba.internal.run_transactions()
        for playlist in _ba.app.config["Free-for-All Playlists"]:
            ba.internal.add_transaction(
                {
                    "type": "REMOVE_PLAYLIST",
                    "playlistType": "Free-for-All",
                    "playlistName": playlist
                })
        ba.internal.run_transactions()
    except Exception as e:
        error_message = f"Error in flush_playlists: {e}"        
        print(error_message)