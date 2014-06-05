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
fanart = 'fanart.jpg'


# Entry point
def run():
    
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
    data = plugintools.read("https://dl.dropboxusercontent.com/u/8036850/palcotvtesst.xml")

    matches = plugintools.find_multiple_matches(data,'<menu_info>(.*?)</menu_info>')
    for entry in matches:
        title = plugintools.find_single_match(entry,'<title>(.*?)</title>')
        date = plugintools.find_single_match(entry,'<date>(.*?)</date>')
        plugintools.add_item( action="" , title = title + date , fanart = art+'fanart.jpg' , thumbnail=art+'icon.png' , folder = False , isPlayable = False )

    data = plugintools.read("https://dl.dropboxusercontent.com/u/8036850/palcotvtesst.xml")
    
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

        elif thumbnail == 'special.png':
            fixed = title
            plugintools.add_item( action = action , plot = fixed , title = '[COLOR lightyellow]' + fixed + '[/COLOR]' , fanart = art+'fanart.jpg' , thumbnail = art + 'special.png' , url = url , folder = True , isPlayable = False )

        elif thumbnail == 'm3u7.png':  # Control para listas M3U
            fixed = title
            plugintools.add_item( action = action , plot = fixed , title = '[COLOR yellowgreen]' + fixed + '[/COLOR]' , fanart = art+'fanart.jpg' , thumbnail = art + 'm3u7.png' , url = url , folder = True , isPlayable = False )

        elif thumbnail == 'xml.png':  # Control para listas XML
            fixed = title
            plugintools.add_item( action = action , plot = fixed , title = '[COLOR lightyellow]' + fixed + '[/COLOR]' , fanart = art+'fanart.jpg' , thumbnail = art + 'xml.png' , url = url , folder = True , isPlayable = False )

        elif thumbnail == 'plx3.png':  # Control para listas PLX
            fixed = title
            plugintools.add_item( action = action , plot = fixed , title = '[COLOR yellowgreen]' + fixed + '[/COLOR]' , fanart = art+'fanart.jpg' , thumbnail = art + 'plx3.png' , url = url , folder = True , isPlayable = False )

        elif thumbnail == 'agenda2.png':  # Control para listas XML
            fixed = title
            plugintools.add_item( action = action , plot = fixed , title = '[COLOR lightyellow]' + fixed + '[/COLOR]' , fanart = art+'fanart.jpg' , thumbnail = art + 'agenda2.png' , url = url , folder = True , isPlayable = False )

        elif thumbnail == 'splive.png':  # Control para listas SPlive
            fixed = title
            plugintools.add_item( action = action , plot = fixed , title = '[COLOR lightyellow]' + fixed + '[/COLOR]' , fanart = art+'fanart.jpg' , thumbnail = art + 'agenda2.png' , url = url , folder = True , isPlayable = False )
        else:
            fixed = title
            plugintools.add_item( action = action, plot = fixed , title = '[COLOR lightyellow]' + fixed + '[/COLOR]' , fanart = art+'fanart.jpg' , thumbnail = art + 'icon.png' , url = url , folder = True , isPlayable = False )
                
                         

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
    if fanart == "":
        fanart = art + 'fanart.jpg'
        
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
    name_channel = params.get("plot")
    plugintools.log("name_channel= "+name_channel)
    pattern = '<name>'+name_channel+'(.*?)</channel>'
    data = plugintools.find_single_match(data, pattern)
    plugintools.add_item( action="" , title='[B][COLOR yellow]'+name_channel+'[/B][/COLOR]' , thumbnail= art + 'special.png' , fanart = art + fanart , folder = False , isPlayable = False )

    subchannel = re.compile('<subchannel>([^<]+)<name>([^<]+)</name>([^<]+)<thumbnail>([^<]+)</thumbnail>([^<]+)<fanart>([^<]+)</fanart>([^<]+)<action>([^<]+)</action>([^<]+)<url>([^<]+)</url>([^<]+)</subchannel>').findall(data)
    for biny, ciny, diny, winy, pixy, dixy, boxy, susy, lexy, muny, kiny in subchannel:
        plugintools.add_item( action = susy , title = ciny , url= muny , thumbnail = winy , fanart = art + fanart , folder = True , isPlayable = False )
        plugintools.log("fanart= "+fanart)
        plugintools.log("thumbnail= "+winy)
        

       
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
        plugintools.add_item( action="play" , title='[COLOR white]'+title+'[/COLOR]' , url=url , thumbnail=art + thumbnail , fanart = art + 'fanart.jpg' , folder = False , isPlayable = True )
        

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
            fanart = plugintools.find_single_match(entry,'<fanart>([^<]+)</fanart>')
            plugintools.add_item( action = "play" , title = title , url = url , thumbnail = thumbnail , fanart = fanart , plot = title , folder = False , isPlayable = True )

    if thumbnail == "name_rtmp.png":
        matches = plugintools.find_multiple_matches(data,'<channel>(.*?)</channel>')
        for entry in matches:
            title = plugintools.find_single_match(entry,'<name>(.*?)</name>')
            url = plugintools.find_single_match(entry,'<rtmp>([^<]+)</rtmp>')
            plugintools.add_item( action = "play" , title = title , url = url , fanart = art + 'fanart.jpg' , plot = title , folder = False , isPlayable = True )

             
def simpletv_items(params):
    plugintools.log("palcoTV.simpletv_items "+repr(params))
    thumbnail = params.get("thumbnail")
    title = params.get("plot")    
    texto= params.get("texto")
    busqueda = ""
    if title == 'search':
        title = title + '.txt'
        plugintools.log("title= "+title)
    else:
        title = title + '.m3u'

    if title == 'search.txt':
        busqueda = 'search.txt'
        file = open(tmp + 'search.txt', "r")
        file.seek(0)
        data = file.readline()
        if data == "":
            ok = plugintools.message("palcoTV", "Sin resultados")
            return ok
    else:
        file = open(playlists + title, "r")
        file.seek(0)
        data = file.readline()
        plugintools.log("data= "+data)
      
    if data == "":
        print "No es posible leer el archivo!"
        data = file.readline()
        plugintools.log("data= "+data)
    else:
        file.seek(0)
        num_items = len(file.readlines())
        print num_items
        plugintools.add_item(action="" , title = '[COLOR lightyellow][B][I]playlist / '+ title +'[/I][/B][/COLOR]' , url = playlists + title , thumbnail = art + "icon.png" , fanart = art + 'fanart.jpg' , folder = False , isPlayable = False)
                           
    # Lectura de items en lista m3u. ToDo: Control de errores, implementar lectura de fanart y thumbnail
    tipo = ""
    i = 0
    file.seek(0)
    data = file.readline()
    while i <= num_items:
        if data.startswith("#EXTINF:-1") == True:
            if busqueda == 'search.txt':
                title = data.replace("#EXTINF:-1", "")
                title = title.replace(",", "")
                title = title.replace("-AZBOX *", "")
                title = title.replace("-AZBOX-*", "")
                title_search = title.split('"')
                titulo = title_search[0]
                origen = title_search[1]
                origen = origen.strip()
            else:
                title = data.replace("#EXTINF:-1", "")
                title = title.replace(",", "")
                title = title.replace("-AZBOX *", "")
                title = title.replace("-AZBOX-*", "")
                title = title.strip()

            if title.startswith(' $ExtFilter="') == True:
                if busqueda == 'search.txt':
                    plugintools.log("lista tipo extfilters= "+title)
                    title = title.replace('$ExtFilter="', "")
                    title_search = title.split('"')
                    titulo = title_search[1]
                    origen = title_search[2]
                    origen = origen.strip()
                    i = i + 1

            if title.startswith('$ExtFilter="') == True:
                if busqueda == 'search.txt':
                    plugintools.log("lista tipo extfilters= "+title)
                    title = title.replace('$ExtFilter="', "")
                    title_search = title.split('"')
                    titulo = title_search[1]
                    origen = title_search[2]
                    origen = origen.strip()
                    i = i + 1
                else:
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
                       
            if title.startswith('group-title="') == True:
                if busqueda == 'search.txt':
                    plugintools.log("lista tipo group-title= "+title)
                    title = title.replace('group-title="', "")
                    title_search = title.split('"')
                    titulo = title_search[0]
                    origen = title_search[1]
                    origen = origen.strip()
                    i = i + 1
                    
                else:
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

            if title.startswith(' tvg-name=') == True:
                if busqueda == 'search.txt':
                    plugintools.log("lista tipo tvg-name= "+title)
                    title = title.replace('tvg-name="', "")
                    title_search = title.split('"')
                    titulo = title_search[0]
                    titulo = titulo.strip()
                    origen = title_search[2]
                    origen = origen.strip()
                    i = i + 1
                    
                else:
                    plugintools.log("lista tipo tvg-name")
                    title = title.replace('tvg-name="', "")
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
                
        if data != "":
            data = data.strip()
            if data.startswith("http") == True:
                print "http"
                url = data.strip()
                if tipo != "":  # Controlamos el caso de subcategoría de canales
                    if busqueda == 'search.txt':
                        plugintools.add_item( action = "play" , title = '[COLOR white] ' + titulo + '[COLOR red] [http][/COLOR][I][COLOR lightyellow] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = art + "icon.png" , fanart = art + 'fanart.jpg' , folder = False , isPlayable = True )
                        data = file.readline()
                        i = i + 1
                        continue
                    else:
                        plugintools.add_item( action = "play" , title = '[COLOR red][I]' + tipo + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR red] [http][/COLOR]' , url = url ,  thumbnail = art + "icon.png" , fanart = art + 'fanart.jpg' , folder = False , isPlayable = True )
                        data = file.readline()
                        i = i + 1
                        continue
                        
                else:
                    if busqueda == 'search.txt':
                        plugintools.add_item( action = "play" , title = '[COLOR white] ' + titulo + '[COLOR red] [http][/COLOR][I][COLOR lightyellow] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = art + "icon.png" , fanart = art + 'fanart.jpg' , folder = False , isPlayable = True )
                        data = file.readline()
                        i = i + 1
                        continue
                    else:
                        plugintools.add_item( action = "play" , title = '[COLOR red][I]' + '[/I][/COLOR][COLOR white] ' + title + '[COLOR red] [http][/COLOR]' , url = url ,  thumbnail = art + "icon.png" , fanart = art + 'fanart.jpg' , folder = False , isPlayable = True )
                        data = file.readline()
                        i = i + 1
                        continue
          
            if data.startswith("rtmp") == True:
                print "rtmp"
                url = data
                url = parse_url(url)
                plugintools.log("url retornada= "+url)
                if tipo != "":  # Controlamos el caso de subcategoría de canales
                    if busqueda == 'search.txt':
                        plugintools.add_item( action = "play" , title = '[COLOR white] ' + titulo + '[COLOR green] [rtmp][/COLOR][I][COLOR lightyellow] (' + origen + ')[/COLOR][/I]', url = url ,  thumbnail = art + "icon.png" , fanart = art + 'fanart.jpg' , folder = False , isPlayable = True )
                        data = file.readline()
                        i = i + 1
                        continue
                    else:
                        plugintools.add_item( action = "play" , title = '[COLOR red][I]' + tipo + ' / [/I][/COLOR][COLOR white] ' + title + '[COLOR green] [rtmp][/COLOR]' , url = url ,  thumbnail = art + "icon.png" , fanart = art + 'fanart.jpg' , folder = False , isPlayable = True )
                        data = file.readline()
                        i = i + 1
                        continue
                        
                else:
                    if busqueda == 'search.txt':
                        plugintools.add_item( action = "play" , title = '[COLOR white] ' + titulo + '[COLOR green] [rtmp][/COLOR][I][COLOR lightyellow] (' + origen + ')[/COLOR][/I]' , url = url ,  thumbnail = art + "icon.png" , fanart = art + 'fanart.jpg' , folder = False , isPlayable = True )
                        data = file.readline()
                        i = i + 1
                        continue
                    else:
                        plugintools.add_item( action = "play" , title = '[COLOR white] ' + title + '[COLOR green] [rtmp][/COLOR]' , url = url ,  thumbnail = art + "icon.png" , fanart = art + 'fanart.jpg' , folder = False , isPlayable = True )
                        data = file.readline()
                        i = i + 1
                        continue
            else:
                data = file.readline()
                i = i + 1
                continue
        else:
            data = file.readline()
            i = i + 1
            

    file.close()
    if title == 'search.txt':
            os.remove(tmp + title)


def myplaylists_m3u(params):  # Mis listas M3U
    plugintools.log("palcoTV.myplaylists_m3u "+repr(params))
    thumbnail = params.get("thumbnail")
    plugintools.add_item(action="play" , title = "[COLOR red][B][Tutorial][/B][COLOR lightyellow]: Importar listas M3U a mi biblioteca [/COLOR][COLOR blue][I][Youtube][/I][/COLOR]" , thumbnail = art + "icon.png" , url = "plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid=8i0KouM-4-U" , folder = False , isPlayable = True )
    plugintools.add_item(action="search_channel" , title = "[B][COLOR lightyellow]Buscador de canales[/COLOR][/B][COLOR lightblue][I] Nuevo![/I][/COLOR]" , thumbnail = art + "search.png" , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )

    ficheros = os.listdir(playlists)  # Lectura de archivos en carpeta /playlists. Cuidado con las barras inclinadas en Windows
    for entry in ficheros:
        plot = entry.split(".")
        plot = plot[0]
        plugintools.log("entry= "+entry)
        if entry.endswith("plx") == True:  # Control para según qué extensión del archivo se elija thumbnail y función a ejecutar
            plugintools.add_item(action="plx_items" , plot = plot , title = entry , url = playlists + entry , thumbnail = art + 'plx3.png' , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )
        else:
            plugintools.add_item(action="simpletv_items" , plot = plot , title = entry , url = playlists + entry , thumbnail = art + 'm3u7.png' , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )

def playlists_m3u(params):  # Biblioteca online
    plugintools.log("palcoTV.playlists_m3u "+repr(params))
    data = plugintools.read( params.get("url") )
    name_channel = params.get("plot")
    pattern = '<name>'+name_channel+'(.*?)</channel>'
    data = plugintools.find_single_match(data, pattern)
    online = '[COLOR yellowgreen][I][Online][/I][/COLOR]'
    params["ext"] = 'm3u'
    plugintools.add_item( action="" , title='[B][COLOR yellow]'+name_channel+'[/B][/COLOR] - [B][I][COLOR lightyellow]juarrox@gmail.com [/COLOR][/B][/I]' , thumbnail= art + 'icon.png' , folder = False , isPlayable = False )
    subchannel = re.compile('<subchannel>([^<]+)<name>([^<]+)</name>([^<]+)<thumbnail>([^<]+)</thumbnail>([^<]+)<url>([^<]+)</url>([^<]+)</subchannel>').findall(data)
    # Sustituir por una lista!!!
    for biny, ciny, diny, winy, pixy, dixy, boxy in subchannel:
        if ciny == "Vcx7 IPTV":
            plugintools.add_item( action="getfile_http" , plot = ciny , title = '[COLOR lightyellow]' + ciny + '[/COLOR] ' + online , url= dixy , thumbnail = art + winy , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )
            params["ext"] = "m3u"
            title = ciny
        elif ciny == "Largo Barbate M3U":
            plugintools.add_item( action="getfile_http" , plot = ciny , title = '[COLOR lightyellow]' + ciny + '[/COLOR] ' + online , url= dixy , thumbnail = art + winy , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )
            title = ciny
        elif ciny == "XBMC Mexico":
            plugintools.add_item( action="getfile_http" , plot = ciny , title = '[COLOR lightyellow]' + ciny + '[/COLOR] ' + online , url= dixy , thumbnail = art + winy , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )
            title = ciny
        elif ciny == "allSat":
            plugintools.add_item( action="getfile_http" , plot = ciny , title = '[COLOR lightyellow]' + ciny + '[/COLOR] ' + online , url= dixy , thumbnail = art + winy , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )
            title = ciny
        elif ciny == "AND Wonder":
            plugintools.add_item( action="getfile_http" , plot = ciny , title = '[COLOR lightyellow]' + ciny + '[/COLOR] ' + online , url= dixy , thumbnail = art + winy , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )
            title = ciny
        elif ciny == "FenixTV":
            plugintools.add_item( action="getfile_http" , plot = ciny , title = '[COLOR lightyellow]' + ciny + '[/COLOR] ' + online , url= dixy , thumbnail = art + winy , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )
            title = ciny
        else:
            plugintools.add_item( action="getfile_http" , plot = ciny , title = '[COLOR lightyellow]' + ciny + '[/COLOR] ' , url= dixy , thumbnail = art + winy , fanart = art + 'fanart.jpg' , folder = True , isPlayable = False )
            title = ciny


    plugintools.log("palcoTV.playlists_m3u "+repr(params))

    
        
def getfile_http(params):  # Descarga de lista M3U + llamada a simpletv_items para que liste los items
    plugintools.log("palcoTV.getfile_http "+repr(params))
    url = params.get("url")
    params["ext"] = "m3u"
    getfile_url(params)
    simpletv_items(params)
   
    
def parse_url(url):
    plugintools.log("url entrante= "+url)

    if url != "":
        url = url.strip()
        url = url.replace("rtmp://$OPT:rtmp-raw=", "")
        # url = url.replace(" --live", "")
        # url = url.replace("conn=S:OK", "")
        # url = url.replace("Conn=S:OK", "")
        # url = url.replace("Conn=S:OK --live", "")
        # url = url.replace("conn=S:OK --live", "")
        # url = url.replace("-live", "")
        # url = url.strip()

        if url.startswith("rtsp") == True:
            url = url.replace("rtsp", "rtmp")
        
       # if url.find("timeout") > 0:
       #     url = url
       # else:
       #     url = url + ' timeout=15'  # En futuras versiones será modificable por el usuario
                    
                                    
        plugintools.log("url saliente= "+url)
        return url
    else:
        plugintools.log("error en url= ")  # Mostrar diálogo de error al parsear url (por no existir, por ejemplo)
        
                    
def getfile_url(params):
    plugintools.log("palcoTV.getfile_url " +repr(params))
    ext = params.get("ext")
    if ext == 'plx':
        filename = params.get("title") + "." + ext  # El título del archivo con extensión (m3u, p2p, plx)
    elif ext == 'm3u':
        filename = params.get("plot") + "." + ext  # El título del archivo con extensión (m3u, p2p, plx)
        
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
    file.seek(0)
    lista_items = {'plot': data}
    file.seek(0)
    


def header_xml(params):
    plugintools.log("palcoTV.header_xml "+repr(params))

    url = params.get("url")
    params.get("title")
    data = plugintools.read(url)
    # plugintools.log("data= "+data)
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

    buscar = params.get("plot")
    plugintools.log("buscar texto: "+buscar)
    if buscar == "":
        last_search = plugintools.get_setting("last_search")
        texto = plugintools.keyboard_input(last_search)
        plugintools.set_setting("last_search",texto)
        params["texto"]=texto
        texto = texto.lower()
        tipo = ""
        if texto == "":
            errormsg = plugintools.message("palcoTV","Por favor, introduzca el canal a buscar")
            return errormsg
        
    else:
        texto = buscar
        texto = texto.lower()
        plugintools.log("texto a buscar= "+texto)
        tipo = ""
    
    results = open(tmp + 'search.txt', "wb")
    results.seek(0)
    results.close()
    print "Cerramos archivo de búsquedas"

    # Listamos archivos de la biblioteca local
    ficheros = os.listdir(playlists)  # Lectura de archivos en carpeta /playlists. Cuidado con las barras inclinadas en Windows
    
    for entry in ficheros:
        if entry.endswith("m3u") == True:
            plot = entry.split(".")
            plot = plot[0]  # plot es la variable que recoge el nombre del archivo (sin extensión txt)
            # Abrimos el primer archivo
            filename = plot + '.m3u'
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
                i = i + 1
                            
                if data.startswith('#EXTINF:-1') == True:
                    data = data.replace('#EXTINF:-1,', "")  # Ignoramos la primera parte de la línea
                    data = data.replace(",", "")
                    title = data.strip()  # Ya tenemos el título
                    minus = title.lower()
                    title = title.replace("-AZBOX*", "")
                    title = title.replace("AZBOX *", "")
                                    
                    if data.startswith('$ExtFilter="') == True:
                        data = data.replace('$ExtFilter="', "")
                        data = data.replace(",", "")
                        data = data.split('"')
                        cat = data[0]
                        cat = cat.strip()
                        title = data[1]
                        title = title.strip()  # Ya tenemos el título
                        minus = title.lower()
                        data = arch.readline()
                        data = data.strip()
                        i = i + 1
                                
                    if title.find('group-title="') >= 0:
                        data = data.replace("group-title=", "")
                        data = data.split('"')
                        cat = data[0]
                        items = len(data)
                        print items
                        items = items - 1
                        title = data[items]
                        title = title.strip()  # Ya tenemos el título
                        minus = title.lower()
                        data = arch.readline()
                        data = data.strip()
                        i = i + 1
                    else:
                        data = arch.readline()
                        data = data.strip()
                        i = i + 1
                                   
                    if minus.find(texto) >= 0:
                    # if re.match(texto, title, re.IGNORECASE):
                        # plugintools.log("Concidencia hallada. Obtenemos url del canal: " + texto)
                        if data.startswith("http") == True:
                            print "URL de tipo 'http'"
                            url = data.strip()
                            if tipo != "":  # Controlamos el caso de subcategoría de canales
                                results = open(tmp + 'search.txt', "a")
                                results.write("#EXTINF:-1," + title + '"' + filename + '\n')
                                results.write(url + '\n\n')
                                results.close()                            
                                data = arch.readline()
                                i = i + 1
                                continue
                            else:
                                results = open(tmp + 'search.txt', "a")
                                results.write("#EXTINF:-1," + title + '"' + filename + '\n')
                                results.write(url + '\n\n')
                                results.close()
                                data = arch.readline()
                                i = i + 1
                                continue
                        if data.startswith("rtmp") == True:
                            print "URL de tipo 'rtmp'"
                            url = data
                            url = parse_url(url)
                            if tipo != "":   # Controlamos el caso de subcategoría de canales
                                results = open(tmp + 'search.txt', "a")
                                results.write("#EXTINF:-1," + title + '"' + filename + '\n')
                                results.write(url + '\n\n')
                                results.close()
                                data = arch.readline()
                                i = i + 1
                                continue
                            else:                            
                                results = open(tmp + 'search.txt', "a")
                                results.write("#EXTINF:-1," + title + '"' + filename + '\n')
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
                                
                  
    arch.close()
    results.close()
    params["plot"] = 'search'  # Pasamos a la lista de variables (params) el valor del archivo de resultados para que lo abra la función simpletv_items
    params['texto']= texto  # Agregamos al diccionario una nueva variable que contiene el texto a buscar
    simpletv_items(params)
    
              



def agendatv(params):
    plugintools.log("palcoTV.agendatv "+repr(params))

    hora_partidos = []
    lista_equipos=[]
    campeonato=[]
    canales=[]

    url = params.get("url")        
    data = plugintools.read(url)
    
    matches = plugintools.find_multiple_matches(data,'<tr>(.*?)</tr>')
    horas = plugintools.find_multiple_matches(data, 'color=#990000>(.*?)</td>')
    txt = plugintools.find_multiple_matches(data, 'color="#000099"><b>(.*?)</td>')
    tv = plugintools.find_multiple_matches(data, '<td align="left"><font face="Verdana, Arial, Helvetica, sans-serif" size="1" ><b>([^<]+)</b></font></td>')

    # <b><a href="indexf.php?comp=Súper Final Argentino">Súper Final Argentino&nbsp;&nbsp;</td>    
    for entry in matches:
        torneo = plugintools.find_single_match(entry, '<a href=(.*?)">')
        torneo = torneo.replace("&nbsp;&nbsp;", "")
        torneo = torneo.replace("indexf.php?comp=", "")
        torneo = torneo.replace('>', "")
        torneo = torneo.replace('"', "")
        torneo = torneo.replace("\n", "")
        torneo = torneo.strip()
        torneo = torneo.replace('\xfa', 'ú')
        torneo = torneo.replace('\xe9', 'é')
        torneo = torneo.replace('\xf3', 'ó')
        torneo = torneo.replace('\xfa', 'ú')
        torneo = torneo.replace('\xaa', 'ª')
        torneo = torneo.replace('\xe1', 'á')
        torneo = torneo.replace('\xf1', 'ñ')
        torneo = torneo.replace('indexuf.php?comp=', "")
        torneo = torneo.replace('indexfi.php?comp=', "")
        plugintools.log("string encoded= "+torneo)
        if torneo != "":
            plugintools.log("torneo= "+torneo)
            campeonato.append(torneo)                    

    # ERROR! Hay que añadir las jornadas, tal como estaba antes!!

    # Vamos a crear dos listas; una de los equipos que se enfrentan cada partido y otra de las horas de juego
    
    for dato in txt:
        lista_equipos.append(dato)
        
    for tiempo in horas:
        hora_partidos.append(tiempo)

    # <td align="left"><font face="Verdana, Arial, Helvetica, sans-serif" size="1" ><b>&nbsp;&nbsp; Canal + Fútbol</b></font></td>
    # <td align="left"><font face="Verdana, Arial, Helvetica, sans-serif" size="1" ><b>&nbsp;&nbsp; IB3</b></font></td>

    for kanal in tv:
        kanal = kanal.replace("&nbsp;&nbsp;", "")
        kanal = kanal.strip()
        kanal = kanal.replace('\xfa', 'ú')
        kanal = kanal.replace('\xe9', 'é')
        kanal = kanal.replace('\xf3', 'ó')
        kanal = kanal.replace('\xfa', 'ú')
        kanal = kanal.replace('\xaa', 'ª')
        kanal = kanal.replace('\xe1', 'á')
        kanal = kanal.replace('\xf1', 'ñ')
        canales.append(kanal)

        
    print lista_equipos
    print hora_partidos  # Casualmente en esta lista se nos ha añadido los días de partido
    print campeonato
    print canales
    
    i = 0       # Contador de equipos
    j = 0       # Contador de horas
    k = 0       # Contador de competición
    max_equipos = len(lista_equipos) - 2
    print max_equipos
    for entry in matches:
        while j <= max_equipos:
            # plugintools.log("entry= "+entry)
            fecha = plugintools.find_single_match(entry, 'color=#990000><b>(.*?)</b></td>')
            fecha = fecha.replace("&#225;", "á")
            fecha = fecha.strip()
            gametime = hora_partidos[i]
            gametime = gametime.replace("<b>", "")
            gametime = gametime.replace("</b>", "")
            gametime = gametime.strip()
            gametime = gametime.replace('&#233;', 'é')
            gametime = gametime.replace('&#225;', 'á')
            gametime = gametime.replace('&#233;', 'é')
            gametime = gametime.replace('&#225;', 'á')  
            print gametime.find(":")
            if gametime.find(":") == 2:
                i = i + 1
                print i
                local = lista_equipos[j]
                local = local.strip()
                local = local.replace('\xfa', 'ú')
                local = local.replace('\xe9', 'é')
                local = local.replace('\xf3', 'ó')
                local = local.replace('\xfa', 'ú')
                local = local.replace('\xaa', 'ª')
                local = local.replace('\xe1', 'á')
                local = local.replace('\xf1', 'ñ')
                j = j + 1
                print j
                visitante = lista_equipos[j]
                visitante = visitante.strip()
                visitante = visitante.replace('\xfa', 'ú')
                visitante = visitante.replace('\xe9', 'é')
                visitante = visitante.replace('\xf3', 'ó')
                visitante = visitante.replace('\xfa', 'ú')
                visitante = visitante.replace('\xaa', 'ª')
                visitante = visitante.replace('\xe1', 'á')
                visitante = visitante.replace('\xf1', 'ñ')
                local = local.replace('&#233;', 'é')
                local = local.replace('&#225;', 'á')  
                j = j + 1
                print j
                tipo = campeonato[k]
                channel = canales[k]
                channel = channel.replace('\xfa', 'ú')
                channel = channel.replace('\xe9', 'é')
                channel = channel.replace('\xf3', 'ó')
                channel = channel.replace('\xfa', 'ú')
                channel = channel.replace('\xaa', 'ª')
                channel = channel.replace('\xe1', 'á')
                channel = channel.replace('\xf1', 'ñ')
                channel = channel.replace('\xc3\xba', 'ú')
                channel = channel.replace('Canal +', 'Canal+')
                title = '[B][COLOR khaki]' + tipo + ':[/B][/COLOR] ' + '[COLOR lightyellow]' + '(' + gametime + ')[COLOR white]  ' + local + ' vs ' + visitante + '[/COLOR][COLOR lightblue][I] (' + channel + ')[/I][/COLOR]'
                plugintools.add_item(plot = channel , action="search_channel", title=title , url = "", fanart = art + 'agenda.jpg', thumbnail = art + 'icon.png' , folder = True, isPlayable = False)
                # diccionario[clave] = valor
                plugintools.log("channel= "+channel)
                params["plot"] = channel
                # plugintools.add_item(plot = channel , action = "search_channel", title = '[COLOR lightblue]' + channel + '[/COLOR]', url= "", thumbnail = art + 'icon.png', fanart = fanart , folder = True, isPlayable = False)
                k = k + 1
                print k
                plugintools.log("title= "+title)
            else:
                plugintools.add_item(action="", title='[B][COLOR red]' + gametime + '[/B][/COLOR]', thumbnail = art + 'icon.png' , fanart = art + 'agenda.jpg' , folder = True, isPlayable = False)
                i = i + 1
        


def encode_string(url):
    

    d = {    '\xc1':'A',
            '\xc9':'E',
            '\xcd':'I',
            '\xd3':'O',
            '\xda':'U',
            '\xdc':'U',
            '\xd1':'N',
            '\xc7':'C',
            '\xed':'i',
            '\xf3':'o',
            '\xf1':'n',
            '\xe7':'c',
            '\xba':'',
            '\xb0':'',
            '\x3a':'',
            '\xe1':'a',
            '\xe2':'a',
            '\xe3':'a',
            '\xe4':'a',
            '\xe5':'a',
            '\xe8':'e',
            '\xe9':'e',
            '\xea':'e',       
            '\xeb':'e',       
            '\xec':'i',
            '\xed':'i',
            '\xee':'i',
            '\xef':'i',
            '\xf2':'o',
            '\xf3':'o',
            '\xf4':'o',   
            '\xf5':'o',
            '\xf0':'o',
            '\xf9':'u',
            '\xfa':'u',
            '\xfb':'u',               
            '\xfc':'u',
            '\xe5':'a'       
    }
   
    nueva_cadena = url
    for c in d.keys():
        plugintools.log("caracter= "+c)
        nueva_cadena = nueva_cadena.replace(c,d[c])

    auxiliar = nueva_cadena.encode('utf-8')
    url = nueva_cadena
    return nueva_cadena



def plx_items(params):
    plugintools.log("palcoTV.plx_items" +repr(params))
    filename = params.get("plot")
    params["plot"]=filename
    params["ext"] = 'plx'
    title = params.get("title")
    fanart = ""
    thumbnail = ""
    
    if title.endswith("plx") == True:
        plugintools.log("Lectura del archivo PLX")
    else:
        getfile_url(params)
        title = params.get("title")
        title = title + '.plx'
        
    file = open(playlists + title, "r")
    file.seek(0)
    num_items = len(file.readlines())
    print num_items
        
    # Lectura del título y fanart de la lista
    file.seek(0)
    i = 0
    data = file.readline()
    while i <= 10:        
        plugintools.log("data= "+data)
        if data.startswith("background=") == True:
            data = data.replace("background=", "")
            fanart = data.strip()
            plugintools.log("fanart= "+fanart)
            i = i + 1
            print i
            data = file.readline()
            continue

        elif data.startswith("title=") == True:
            name = data.replace("title=", "")
            name = name.strip()
            plugintools.log("name= "+name)
            i = i + 1
            print i
            data = file.readline()
            continue

        elif data.startswith("logo=") == True:
            data = data.replace("logo=", "")
            thumbnail = data.strip()
            plugintools.log("thumbnail= "+thumbnail)
            i = i + 1
            print i
            data = file.readline()
            continue

        else:
            i = i + 1
            data = file.readline()
            print i


    if fanart == "":
        fanart = art + 'fanart.jpg'

    if thumbnail == "":
        thumbnail = art + 'plx3.png'

    

    plugintools.add_item(action="" , title = '[COLOR lightyellow][B][I]playlist / '+ title +'[/I][/B][/COLOR]' , url = playlists + title , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = False)
    plugintools.add_item(action="" , title = '[I][B]' + name + '[/B][/I]' , url = "" , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = False)
            
    try:        
        data = file.readline()
        plugintools.log("data= "+data)
        if data.startswith("background=") == True:
            data = data.replace("background=", "")
            data = data.strip()
            fanart = data
            plugintools.log("fanart= "+fanart)
        else:
            # data = file.readline()
            if data.startswith("background=") == True:
                print "Archivo plx!"
                data = data.replace("background=", "")
                fanart = data.strip()
                plugintools.log("fanart= "+fanart)
            else:
                if data.startswith("title=") == True:
                    name = data.replace("title=", "")
                    name = name.strip()
                    plugintools.log("name= "+name)
    except:
        plugintools.log("ERROR: Unable to load PLX file")


    data = file.readline()
    try:
        if data.startswith("title=") == True:
            data = data.replace("title=", "")
            name = data.strip()            
            plugintools.log("title= "+title)
            plugintools.add_item(action="" , title = '[COLOR lightyellow][B][I]playlist / '+ title +'[/I][/B][/COLOR]' , url = playlists + title , thumbnail = art + "icon.png" , fanart = fanart , folder = False , isPlayable = False)
            plugintools.add_item(action="" , title = '[I][B]' + name + '[/B][/I]' , url = "" , thumbnail = art + "icon.png" , fanart = fanart , folder = False , isPlayable = False)
    except:
        plugintools.log("Unable to read PLX title")

    i = 0
    file.seek(0)
          
    # Lectura de items
    while i <= num_items:
        data = file.readline()
        data = data.strip()
        i = i + 1
        print i
        if data.startswith("#") == True:
            continue
        
        if (data == 'type=video') or (data == 'type=audio') == True:
            data = file.readline()
            i = i + 1
            print i
            data = data.replace("name=", "")
            data = data.strip()
            title = data
            plugintools.log("title= "+title)
            data = file.readline()
            i = i + 1
            print i
            
            if data.startswith("thumb") == True:
                data = data.replace("thumb=", "")
                data = data.strip()
                thumbnail = data
                plugintools.log("thumbnail= "+thumbnail)
                data = file.readline()
                i = i + 1
                print i
                data = data.replace("URL=", "")
                data = data.strip()
                url = data
                parse_url(url)
                plugintools.log("URL= "+url)
                data = file.readline()
                i = i + 1
                print i
                plugintools.log("url= "+url)
                plugintools.add_item(action="play" , title = title , url = url , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True)
                continue
                
            elif data.startswith("date") == True:
                data = file.readline()
                i = i + 1
                print i
                if data.startswith("URL") == True:
                    data = data.replace("URL=", "")                    
                    url = data.strip()
                    parse_url(url)
                    plugintools.log("URL= "+url)
                    data = file.readline()
                    i = i + 1
                    print i
                    plugintools.log("url= "+url)
                    if thumbnail == "":
                        thumbnail = art + 'plx3.png'
                        
                    plugintools.add_item(action="play" , title = title , url = url , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True)
                    continue
                else:
                    if data.startswith("thumb") == True:
                        data = data.replace("thumb=", "")
                        data = data.strip()
                        thumb = data
                        data = file.readline()
                        i = i + 1
                        print i
                        url = data.strip()
                        parse_url(url)
                        plugintools.log("URL= "+url)
                        data = file.readline()
                        i = i + 1
                        print i
                        plugintools.add_item(action="play" , title = title , url = url , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True)
                        continue
                                        
            else:
                if data.startswith("URL") == True:
                    data = data.replace("URL=", "")
                    data = data.strip()
                    url = data
                    parse_url(url)
                    plugintools.log("URL= "+url)
                    data = file.readline()
                    i = i + 1
                    print i
                    plugintools.log("url= "+url)
                    plugintools.add_item(action="play" , title = title , url = url , thumbnail = thumbnail , fanart = fanart , folder = False , isPlayable = True)
                    continue

        else:
            i = i + 1
            print i
            data = file.readline()
            plugintools.log("data= "+data)
           

    file.close()

             
    

run()

