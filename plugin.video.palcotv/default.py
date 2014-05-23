# -*- coding: utf-8 -*-
#------------------------------------------------------------
# palcoTV - XBMC Add-on by Juarrox (juarrox@gmail.com)
# Version 0.2.5 (15.05.2014)
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Gracias a la librería plugintools de Jesús (www.mimediacenter.info)


import os
import sys
import urllib
import urllib2
import re

import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin

import plugintools


art = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.palcotv/art', ''))
playlists = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.palcotv/playlists', ''))
tmp = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.palcotv/tmp', ''))
icon = art + 'icon.png'
fanart = art + 'fanart.jpg'


# Entry point
def run():

    # icon = 'icon.png'
    # fanart = 'fanart.png'
    
    plugintools.log("---> palcoTV.run <---")
    plugintools.set_view(plugintools.LIST)
    
    # Get params
    params = plugintools.get_params()
    
    if params.get("action") is None:
        main_list(params)
    else:
       action = params.get("action")
       url = params.get("url")
       exec action+"(params)"

    plugintools.close_item_list()
       
  
# Main menu

def main_list(params):
    plugintools.log("palcoTV.main_list "+repr(params))
    data = plugintools.read("https://dl.dropboxusercontent.com/u/8036850/palcotvtest.xml")

    matches = plugintools.find_multiple_matches(data,'<menu_info>(.*?)</menu_info>')
    for entry in matches:
        title = plugintools.find_single_match(entry,'<title>(.*?)</title>')
        date = plugintools.find_single_match(entry,'<date>(.*?)</date>')
        plugintools.add_item( action="" , title = title + date , fanart = art+'fanart.jpg' , thumbnail=art+'icon.png' , folder = False , isPlayable = False )

    data = plugintools.read("https://dl.dropboxusercontent.com/u/8036850/palcotvtest.xml")
    
    matches = plugintools.find_multiple_matches(data,'<channel>(.*?)</channel>')
    for entry in matches:
        title = plugintools.find_single_match(entry,'<name>(.*?)</name>')
        thumbnail = plugintools.find_single_match(entry,'<thumbnail>(.*?)</thumbnail>')
        fanart = plugintools.find_single_match(entry,'<fanart>(.*?)</fanart>')
        action = plugintools.find_single_match(entry,'<action>(.*?)</action>')
        last_update = plugintools.find_single_match(entry,'<last_update>(.*?)</last_update>')
        url = plugintools.find_single_match(entry,'<url>(.*?)</url>')
        date = plugintools.find_single_match(entry,'<last_update>(.*?)</last_update>')
        if thumbnail == 'new.png':
            fixed = title
            plugintools.add_item( action = action , plot = fixed , title = '[COLOR lightyellow]' + fixed + '[/COLOR]' , fanart = art+'fanart.jpg' , thumbnail = art + 'new.png' , url = url , folder = True , isPlayable = False )
        else:
            if thumbnail == 'm3u.png':  # Control para listas M3U
                fixed = title
                plugintools.add_item( action = action , plot = fixed , title = '[COLOR skyblue]' + fixed + '[/COLOR]' , fanart = art+'fanart.jpg' , thumbnail = art + 'm3u.png' , url = url , folder = True , isPlayable = False )

            if thumbnail == 'special.png':  # Control para listas XML
                fixed = title
                plugintools.add_item( action = action , plot = fixed , title = '[COLOR lightyellow]' + fixed + '[/COLOR]' , fanart = art+'fanart.jpg' , thumbnail = art + 'm3u.png' , url = url , folder = True , isPlayable = False )
                
                         

def play(params):
    plugintools.play_resolved_url( params.get("url") )


def runPlugin(url):
    xbmc.executebuiltin('XBMC.RunPlugin(' + url +')')


def live_items_withlink(params):
    plugintools.log("palcoTV.live_items_withlink "+repr(params))
    data = plugintools.read(params.get("url"))

    # ToDo: Agregar función lectura de cabecera (fanart, thumbnail, título, últ. actualización)
    header_xml(params)

    fanart = plugintools.find_single_match(data, '<fanart>(.*?)</fanart>')  # Localizamos fanart de la lista
    author = plugintools.find_single_match(data, '<poster>(.*?)</poster>')  # Localizamos autor de la lista (encabezado)
    
    matches = plugintools.find_multiple_matches(data,'<item>(.*?)</item>')
    for entry in matches:
        title = plugintools.find_single_match(entry,'<title>(.*?)</title>')
        title = title.replace("<![CDATA[", "")
        title = title.replace("]]>", "")
        thumbnail = plugintools.find_single_match(entry,'<thumbnail>(.*?)</thumbnail>')
        url = plugintools.find_single_match(entry,'<link>(.*?)</link>')
        url = url.replace("<![CDATA[", "")
        url = url.replace("]]>", "")
        plugintools.add_item(action = "play" , title = title , url = url , fanart = fanart , folder = False , isPlayable = True )
        

  
def xml_lists(params):
    plugintools.log("palcoTV.xml_listas "+repr(params))
    data = plugintools.read( params.get("url") )
    plugintools.log("url= "+data)
    name_channel = params.get("plot")
    plugintools.log("name_channel= "+name_channel)
    pattern = '<name>'+name_channel+'(.*?)</channel>'
    data = plugintools.find_single_match(data, pattern)
    plugintools.log("data= "+data)
    plugintools.add_item( action="" , title='[B][COLOR yellow]'+name_channel+'[/B][/COLOR]' , thumbnail= art + 'splive.png' , folder = False , isPlayable = False )

    subchannel = re.compile('<subchannel>([^<]+)<name>([^<]+)</name>([^<]+)<thumbnail>([^<]+)</thumbnail>([^<]+)<fanart>([^<]+)</fanart>([^<]+)<action>([^<]+)</action>([^<]+)<url>([^<]+)</url>([^<]+)</subchannel>').findall(data)
    for biny, ciny, diny, winy, pixy, dixy, boxy, susy, lexy, muny, kiny in subchannel:
        plugintools.add_item( action = susy , title = ciny , url= muny , thumbnail = winy , fanart = dixy , folder = True , isPlayable = False )        

       
def getstreams_now(params):
    plugintools.log("palcoTV.getstreams_now "+repr(params))
    
    data = plugintools.read( params.get("url") )
    poster = plugintools.find_single_match(data, '<poster>(.*?)</poster>')
    plugintools.add_item(action="" , title='[COLOR blue][B]'+poster+'[/B][/COLOR]', url="", folder =False, isPlayable=False)
    matches = plugintools.find_multiple_matches(data,'<title>(.*?)</link>')
    
    for entry in matches:
        title = plugintools.find_single_match(entry,'(.*?)</title>')
        url = plugintools.find_single_match(entry,'<link> ([^<]+)')
        plugintools.add_item( action="play" , title=title , url=url , folder = False , isPlayable = True )
        
      
def p2plinks(params):
    plugintools.log("palcoTV.livetv "+repr(params))
      
    data = plugintools.read( params.get("url") )
    matches = plugintools.find_multiple_matches(data,'<item>(.*?)</item>')
    for entry in matches:
        title = plugintools.find_single_match(entry,'<title>(.*?)</title>')
        thumbnail = plugintools.find_single_match(entry,'<thumbnail>(.*?)</thumbnail>')
        ace_url = plugintools.find_single_match(entry,'<link>(.*?)</link>')
        last_update = plugintools.find_single_match(entry,'<date>(.*?)</date>')
        url = 'plugin://plugin.video.p2p-streams/?url=' + ace_url + '&mode=1&name=' + title + ')'
        plugintools.add_item( action="play" , title='[COLOR white]'+title+'[/COLOR]' , url=url , thumbnail=art + thumbnail , folder = False , isPlayable = True )
        

# Soporte de listas de canales por categorías (Livestreams, XBMC México, Motor SportsTV, etc.). 

def livestreams_channels(params):
    plugintools.log("palcoTV.livestreams_channels "+repr(params))
    data = plugintools.read( params.get("url") )
       
    # Extract directory list
    thumbnail = params.get("thumbnail")
    
    if thumbnail == "":
        thumbnail = 'icon.jpg'
        plugintools.log(thumbnail)
    else:
        plugintools.log(thumbnail)
    
    if thumbnail == art + 'icon.png':
        matches = plugintools.find_multiple_matches(data,'<channel>(.*?)</channel>')
        for entry in matches:
            title = plugintools.find_single_match(entry,'<name>(.*?)</name>')
            thumbnail = plugintools.find_single_match(entry,'<thumbnail>(.*?)</thumbnail>')
            fanart = plugintools.find_single_match(entry,'<fanart>(.*?)</fanart>')
            plugintools.add_item( action="livestreams_subchannels" , title=title , url=params.get("url") , thumbnail=thumbnail , fanart=fanart , folder = True , isPlayable = False )

    else:
        matches = plugintools.find_multiple_matches(data,'<channel>(.*?)</channel>')
        for entry in matches:
            title = plugintools.find_single_match(entry,'<name>(.*?)</name>')
            thumbnail = plugintools.find_single_match(entry,'<thumbnail>(.*?)</thumbnail>')
            fanart = plugintools.find_single_match(entry,'<fanart>(.*?)</fanart>')
            plugintools.add_item( action="livestreams_items" , title=title , url=params.get("url") , fanart=fanart , thumbnail=thumbnail , folder = True , isPlayable = False )
   
        
def livestreams_subchannels(params):
    plugintools.log("palcoTV.livestreams_subchannels "+repr(params))

    data = plugintools.read( params.get("url") )
    # title_channel = params.get("title")
    title_channel = params.get("title")
    name_subchannel = '<name>'+title_channel+'</name>'
    data = plugintools.find_single_match(data, name_subchannel+'(.*?)</channel>')
    info = plugintools.find_single_match(data, '<info>(.*?)</info>')
    title = params.get("title")
    plugintools.set_view(plugintools.LIST)
    plugintools.add_item( action="" , title='[B]'+title+'[/B] [COLOR yellow]'+info+'[/COLOR]' , folder = False , isPlayable = False )

    subchannel = plugintools.find_multiple_matches(data , '<name>(.*?)</name>')
    for entry in subchannel:
        plugintools.add_item( action="livestreams_subitems" , title=entry , url=params.get("url") , thumbnail=art+'motorsports-xbmc.jpg' , folder = True , isPlayable = False )


# Pendiente de cargar thumbnail personalizado y fanart...
def livestreams_subitems(params):
    plugintools.log("palcoTV.livestreams_subitems "+repr(params))

    title_subchannel = params.get("title")
    data = plugintools.read( params.get("url") )
    source = plugintools.find_single_match(data , title_subchannel+'(.*?)<subchannel>')

    titles = re.compile('<title>([^<]+)</title>([^<]+)<link>([^<]+)</link>').findall(source)
    url = params.get("url")
    title = params.get("title")
    thumbnail = params.get("thumbnail")
    
    for entry, quirry, winy in titles:
        winy = winy.replace("amp;","")
        plugintools.add_item( action="play" , title = entry , url = winy , thumbnail = thumbnail , folder = False , isPlayable = True )


def livestreams_items(params):
    plugintools.log("palcoTV.livestreams_items "+repr(params))

    title_subchannel = params.get("title")
    title_subchannel_fixed = plugintools.find_single_match(title_subchannel, ']([^[]+)')
    
    if title_subchannel_fixed == "":
        title_subchannel_fixed = title_subchannel
    else:
        plugintools.log("titulo categoria fixed= "+title_subchannel_fixed)
           
    data = plugintools.read( params.get("url") )
    
    pattern = title_subchannel_fixed+'(.*?)channel>'
    source = plugintools.find_single_match(data , pattern)

    titles = re.compile('<title>([^<]+)</title>([^<]+)<link>([^<]+)</link>([^<]+)<thumbnail>([^<]+)</thumbnail>').findall(source)
    
    url = params.get("url")
    title = params.get("title")
    thumbnail = params.get("thumbnail")
    
    for entry, quirry, winy, xiry, miry in titles:
        winy = winy.replace("amp;","")
        plugintools.add_item( action="play" , title = entry , url = winy , thumbnail = miry , folder = False , isPlayable = True )


def xml_items(params):
    plugintools.log("palcoTV.xml_items "+repr(params))
    data = plugintools.read( params.get("url") )
    thumbnail = params.get("thumbnail")

    #Todo: Implementar una variable que permita seleccionar qué tipo de parseo hacer
    if thumbnail == "title_link.png":
        matches = plugintools.find_multiple_matches(data,'<item>(.*?)</item>')
        for entry in matches:
            title = plugintools.find_single_match(entry,'<title>(.*?)</title>')
            thumbnail = plugintools.find_single_match(entry,'<thumbnail>(.*?)</thumbnail>')
            url = plugintools.find_single_match(entry,'<link>([^<]+)</link>')
            plugintools.add_item( action = "play" , title = title , url = url , thumbnail = thumbnail , folder = False , isPlayable = True )

    if thumbnail == "name_rtmp.png":
        matches = plugintools.find_multiple_matches(data,'<channel>(.*?)</channel>')
        for entry in matches:
            title = plugintools.find_single_match(entry,'<name>(.*?)</name>')
            url = plugintools.find_single_match(entry,'<rtmp>([^<]+)</rtmp>')
            plugintools.add_item( action = "play" , title = title , url = url , folder = False , isPlayable = True )

             
def simpletv_items(params):
    plugintools.log("palcoTV.simpletv_items "+repr(params))
    thumbnail = params.get("thumbnail")
    title = params.get("plot")
    title = title + '.txt'
    if title != 'search.txt':
        file = open(playlists + title, "r")
        file.seek(0)
        data = file.readline()
    else:
        file = open(tmp + 'search.txt', "r")
        file.seek(0)
        data = file.readline()
    
    if data != -1:
        file.seek(0)
        num_items = len(file.readlines())
        plugintools.add_item(action="" , title = '[COLOR lightyellow][B][I]playlist / '+ title +'[/I][/B][/COLOR]' , url = playlists + title , folder = False , isPlayable = False )
        print num_items
                
    # Lectura de items en lista m3u. ToDo: Control de errores, implementar lectura de fanart y thumbnail
    tipo = ""
    i = 0
    file.seek(0)
    data = file.readline()
    while i <= num_items:
        if data.startswith("#EXTINF:-1") == True:
            plugintools.log("linea= "+data)
            plugintools.log("title= "+title)
            title = data.replace("#EXTINF:-1", "")
            title = title.replace(",", "")
            title = title.replace("-AZBOX *", "")
            title = title.replace("-AZBOX-*", "")
            title = title.strip()
            plugintools.log("title= "+title)
            plugintools.log("title-channel= "+title)            
            plugintools.log("data= "+data)
            if title.startswith('$ExtFilter="') == True:
                plugintools.log("lista tipo extfilters")
                title = title.replace('$ExtFilter="', "")
                category = title.split('"')
                tipo = category[0]
                tipo = tipo.strip()
                title = category[1]
                title = title.strip()
                print title
                plugintools.log("title_shannel= "+title)
                data = file.readline()
                i = i + 1
                print i           
                            
            if title.startswith('group-title="') == True:
                plugintools.log("lista tipo group-title")
                title = title.replace('group-title="', "")
                category = title.split('"')
                items = len(category)
                print category
                tipo = category[0]  # tipo= categoría o sección de canales
                tipo = tipo.strip()
                plugintools.log("tipo= "+tipo)
                items = items - 1
                title = category[items]
                title = title.strip()
                plugintools.log("title_vhannel= "+title)
                data = file.readline()
                i = i + 1
                print i
                
        if data != "":
            data = data.strip()
            if data.startswith("http") == True:
                print "http"
                url = data.strip()
                if tipo != "":  # Controlamos el caso de subcategoría de canales
                    plugintools.add_item( action = "play" , title = '[COLOR red][I]' + tipo + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR green] [http][/COLOR]', url = url ,  thumbnail = art + 'icon.png' , fanart = fanart , folder = False , isPlayable = True )
                    plugintools.log("title= "+title)
                    plugintools.log("url_http_con_tipo= "+url)
                    data = file.readline()
                    i = i + 1
                    print i
                    continue
                else:
                    plugintools.add_item( action = "play" , title = '[COLOR white] ' + title + '[/COLOR][COLOR green] [http][/COLOR]', url = url ,  thumbnail = art + 'icon.png' , fanart = fanart , folder = False , isPlayable = True )
                    plugintools.log("title= "+title)
                    plugintools.log("url_http_sin_tipo= "+url)
                    data = file.readline()
                    i = i + 1
                    continue
          
            if data.startswith("rtmp") == True:
                print "rtmp"
                url = data
                url = parse_url(url)
                plugintools.log("url retornada= "+url)
                if tipo != "":   # Controlamos el caso de subcategoría de canales
                    plugintools.add_item( action = "play" , title = '[COLOR red][I]' + tipo + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR green] [rtmp][/COLOR]', url = url ,  thumbnail = art + 'icon.png' , fanart = fanart , folder = False , isPlayable = True )
                    plugintools.log("title= "+title)
                    plugintools.log("url_rtmp_con_tipo= "+url)
                    data = file.readline()
                    i = i + 1
                    print i
                    continue
                else:
                    plugintools.add_item( action = "play" , title = '[COLOR white] ' + title + '[/COLOR][COLOR green] [rtmp][/COLOR]' , url = url , thumbnail = art + 'icon.png' , fanart = fanart , folder = False , isPlayable = True )
                    plugintools.log("title= "+title)
                    plugintools.log("url_rtmp_sin_tipo= "+url)
                    data = file.readline()
                    i = i + 1
                    print i
                    continue
            else:
                data = file.readline()
                i = i + 1
                print i
                continue
        else:
            data = file.readline()
            i = i + 1
            print i

    file.close()
    if title == 'search.txt':
        os.remove(tmp + title)



def myplaylists_m3u(params):  # Mis listas M3U
    plugintools.log("palcoTV.myplaylists_m3u "+repr(params))
    thumbnail = params.get("thumbnail")
    plugintools.add_item(action="play" , title = "[COLOR red][B][Tutorial][/B][COLOR lightyellow]: Importar listas M3U a mi biblioteca [/COLOR][COLOR blue][I][Youtube][/I][/COLOR]" , thumbnail = art + "icon.png" , url = "plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid=8i0KouM-4-U" , folder = False , isPlayable = True )
    plugintools.add_item(action="search_channel" , title = "[B][COLOR lightyellow]Buscador de canales[/COLOR][/B][COLOR lightblue][I] Nuevo![/I][/COLOR]" , thumbnail = art + "search.png" , fanart = fanart , folder = True , isPlayable = False )

    ficheros = os.listdir(playlists)  # Lectura de archivos en carpeta /playlists. Cuidado con las barras inclinadas en Windows
    for entry in ficheros:
        plot = entry.split(".")
        plot = plot[0]
        plugintools.add_item(action="simpletv_items" , plot = plot , title = entry , url = playlists + entry , thumbnail = thumbnail , fanart = fanart , folder = True , isPlayable = False )

def playlists_m3u(params):  # Biblioteca online
    plugintools.log("palcoTV.playlists_m3u "+repr(params))
    data = plugintools.read( params.get("url") )
    name_channel = params.get("plot")
    plugintools.log("name_channel= "+name_channel)
    pattern = '<name>'+name_channel+'(.*?)</channel>'
    data = plugintools.find_single_match(data, pattern)
    online = '[COLOR yellowgreen][I][Online][/I][/COLOR]'
    plugintools.add_item( action="" , title='[B][COLOR yellow]'+name_channel+'[/B][/COLOR] - [B][I][COLOR lightyellow]juarrox@gmail.com [/COLOR][/B][/I]' , thumbnail= art + 'icon.png' , folder = False , isPlayable = False )
    subchannel = re.compile('<subchannel>([^<]+)<name>([^<]+)</name>([^<]+)<thumbnail>([^<]+)</thumbnail>([^<]+)<url>([^<]+)</url>([^<]+)</subchannel>').findall(data)
    for biny, ciny, diny, winy, pixy, dixy, boxy in subchannel:
        if ciny == "Vcx7 IPTV":
            plugintools.add_item( action="getfile_http" , plot = ciny , title = '[COLOR lightyellow]' + ciny + '[/COLOR] ' + online , url= dixy , thumbnail = art + winy , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )
            title = ciny
        elif ciny == "Largo Barbate M3U":
            plugintools.add_item( action="getfile_http" , plot = ciny , title = '[COLOR lightyellow]' + ciny + '[/COLOR] ' + online , url= dixy , thumbnail = art + winy , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )
            title = ciny
        elif ciny == "XBMC Mexico":
            plugintools.add_item( action="getfile_http" , plot = ciny , title = '[COLOR lightyellow]' + ciny + '[/COLOR] ' + online , url= dixy , thumbnail = art + winy , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )
            title = ciny
        else:
            plugintools.add_item( action="getfile_http" , plot = ciny , title = '[COLOR lightyellow]' + ciny + '[/COLOR] ' , url= dixy , thumbnail = art + winy , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )
            title = ciny
            
        
def getfile_http(params):  # Descarga de lista M3U + llamada a simpletv_items para que liste los items
    plugintools.log("palcoTV.getfile_http "+repr(params))
    url = params.get("url")

    if url.startswith("https://dl.dropboxusercontent.com/u/") == True:
        print "vamos a getfile_url"
        print "nos quedamos aqui que es dropbox"
        file = urllib2.urlopen(url)
        size_bytes = file.info()
        filesize = size_bytes.getheaders("Content-Length")[0]
        filesize = int(filesize) * 1024
        plugintools.log("filesize= "+repr(filesize))
        byte = 1
        filename = params.get("plot") + '.txt'
        arch = open(playlists + filename, 'wb')
        arch.seek(0)
        lista_items = {'title': filename, 'url': filename, 'thumbnail': art + 'icon.png'}        
        while (byte != filesize):  # TODO: Añadir cuadro de diálogo de espera
            arch.write(file.read(byte))
            byte = byte + 1           

        arch.close()      # Cerramos archivo remoto y abrimos el archivo creado
        plot = params.get("plot")
        filename = plot + '.txt'
        file = open(playlists + filename, "r")
        file.seek(0)
        data = file.readline()
        data = data.strip()        
        lista_items = {'linea': data}
        lista_items = {'plot': data}
        simpletv_items(params)
    else:
        getfile_url(params)
      

    
def parse_url(url):
    plugintools.log("url entrante= "+url)

    if url != "":
        # url = url.strip()
        # url = url.replace("rtmp://$OPT:rtmp-raw=", "")
        # url = url.replace("conn=S:OK", "")
        # url = url.replace("Conn=S:OK", "")
        # url = url.replace("Conn=S:OK --live", "")
        # url = url.replace("conn=S:OK --live", "")
        # url = url.replace("--live", "")
        # url = url.replace("-live", "")
        # url = url.strip()
        
        if url.find("timeout") >= 0:
                    url = url + ' timeout=15'  # En futuras versiones será modificable por el usuario
                                    
        plugintools.log("url saliente= "+url)
        return url
    else:
        plugintools.log("error en url= ")  # Mostrar diálogo de error al parsear url (por no existir, por ejemplo)
        
                    
def getfile_url(params):
    plugintools.log("palcoTV.getfile_url " +repr(params))
    filename = params.get("plot") + '.txt'  # El título del canal sin formato
    plugintools.log("filename= "+filename)
    url = params.get("url")
    plugintools.log("url= "+url)
    response = urllib2.urlopen(url)

    #open the file for writing
    fh = open(playlists + filename, "wb")

    # read from request while writing to file
    fh.write(response.read())

    fh.close()

    file = open(playlists + filename, "r")
    file.seek(0)
    data = file.readline()
    data = data.strip()

    lista_items = {'linea': data}
    
    if data == '﻿#P2P':
        playlist_p2p(params)
        file.seek(0)
    else:
        lista_items = {'plot': data}
        file.seek(0)
        simpletv_items(params)


def header_xml(params):
    plugintools.log("palcoTV.header_xml "+repr(params))

    url = params.get("url")
    params.get("title")
    data = plugintools.read(url)
    plugintools.log("data= "+data)
    author = plugintools.find_single_match(data, '<poster>(.*?)</poster>')
    author = author.strip()
    fanart = plugintools.find_single_match(data, '<fanart>(.*?)</fanart>')
    message = plugintools.find_single_match(data, '<message>(.*?)</message>')
    desc = plugintools.find_single_match(data, '<description>(.*?)</description>')
    thumbnail = plugintools.find_single_match(data, '<thumbnail>(.*?)</thumbnail>')
    
    if author != "":
        if message != "":
            plugintools.add_item(action="" , plot = author , title = '[COLOR green][B]' + author + '[/B][/COLOR][I] ' + message + '[/I]', url = "" , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = False )
            return fanart
        else:
            plugintools.add_item(action="" , plot = author , title = '[COLOR green][B]' + author + '[/B][/COLOR]', url = "" , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = False )
            return fanart
    else:
        if desc != "":
            plugintools.add_item(action="" , plot = author , title = '[COLOR green][B]' + desc + '[/B][/COLOR]', url = "" , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = False )
            return fanart
        else:
            return fanart


def search_channel(params):
    plugintools.log("palcoTV.search " + repr(params))

    last_search = plugintools.get_setting("last_search")
    texto = plugintools.keyboard_input(last_search)
    plugintools.set_setting("last_search",texto)
    params["texto"]=texto
    plugintools.log("texto a buscar= "+texto)
    tipo = 0
    
    if texto == "":
        plugintools.log("Texto vacío. Saliendo...")
        errormsg = plugintools.message("palcoTV","Por favor, introduzca el canal a buscar")
        return errormsg

    results = open(tmp + 'search.txt', "wb")
    results.seek(0)
    results.close()

    # Listamos archivos de la biblioteca local
    ficheros = os.listdir(playlists)  # Lectura de archivos en carpeta /playlists. Cuidado con las barras inclinadas en Windows
    
    for entry in ficheros:        
        plot = entry.split(".")
        plot = plot[0]  # plot es la variable que recoge el nombre del archivo (sin extensión txt)
        # Abrimos el primer archivo
        filename = plot + '.txt'
        arch = open(playlists + filename, "r")
        num_items = len(arch.readlines())
        plugintools.log("archivo= "+filename)
        i = 0  # Controlamos que no se salga del bucle while antes de que lea el último registro de la lista
        arch.seek(0)
        data = arch.readline()
        data = data.strip()
        texto = texto.strip()
        plugintools.log("data_antes= "+data)
        while i <= num_items:                                     
            data = arch.readline()
            plugintools.log("data_dentro= "+data)
            i = i + 1
                        
            if data.startswith('#EXTINF:-1') == True:
                data = data.replace('#EXTINF:-1,', "")  # Ignoramos la primera parte de la línea
                data = data.replace(",", "")
                title = data.strip()  # Ya tenemos el título
                title = title.replace("-AZBOX*", "")
                title = title.replace("AZBOX *", "")
                plugintools.log("title_extinf= "+title)
                
                if data.startswith('$ExtFilter="') == True:
                    data = data.replace('$ExtFilter="', "")
                    data = data.replace(",", "")
                    data = data.split('"')
                    cat = data[0]
                    cat = cat.strip()
                    title = data[1]
                    title = title.strip()  # Ya tenemos el título
                    plugintools.log("title_extfilter= "+title)
                    plugintools.log("data_extfilter= "+data)
                    data = arch.readline()
                    data = data.strip()
                    i = i + 1
                            
                if title.find('group-title="') >= 0:
                    data = data.replace("group-title=", "")
                    data = data.split('"')
                    cat = data[0]
                    items = len(cat)
                    print cat                    
                    plugintools.log("title_pre= "+title)
                    title = title.strip()  # Ya tenemos el título
                    plugintools.log("title_grouptitle= "+title)
                    data = arch.readline()
                    data = data.strip()
                    i = i + 1
                else:
                    data = arch.readline()
                    data = data.strip()
                    i = i + 1
                               
                if title.find(texto) >= 0:
                # if re.match(texto, title, re.IGNORECASE):
                    plugintools.log("Concidencia hallada. Obtenemos url del canal: " + texto)
                    plugintools.log("Linea url= "+data)
                    if data.startswith("http") == True:
                        print "URL de tipo 'http'"
                        url = data.strip()
                        if tipo != "":  # Controlamos el caso de subcategoría de canales
                            results = open(tmp + 'search.txt', "a")
                            results.write("#EXTINF:-1," + title + '\n')
                            results.write(url + '\n\n')
                            results.close()                            
                            data = arch.readline()
                            i = i + 1
                            continue
                        else:
                            results = open(tmp + 'search.txt', "a")
                            results.write("#EXTINF:-1," + title + '\n')
                            results.write(url + '\n\n')
                            results.close()
                            data = arch.readline()
                            i = i + 1
                            continue
                    if data.startswith("rtmp") == True:
                        print "URL de tipo 'http'"
                        url = data
                        url = parse_url(url)
                        plugintools.log("url retornada= "+url)
                        if tipo != "":   # Controlamos el caso de subcategoría de canales
                            results = open(tmp + 'search.txt', "a")
                            results.write("#EXTINF:-1," + title + '\n')
                            results.write(url + '\n\n')
                            results.close()
                            data = arch.readline()
                            i = i + 1
                            continue
                        else:                            
                            results = open(tmp + 'search.txt', "a")
                            results.write("#EXTINF:-1," + title + '\n')
                            results.write(url + '\n\n')
                            results.close()
                            data = arch.readline()
                            i = i + 1
                            continue
            else:
                data = arch.readline()
                data = data.strip()
                i = i + 1
                print i
                                
                  

    params["plot"] = 'search'  # Pasamos a la lista de variables (params) el valor del archivo de resultados para que lo abra la función simpletv_items
    simpletv_items(params)
              


             
        
run()

