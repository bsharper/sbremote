import os
import json
import time
import sponsorblock as sb
from youtubesearchpython import VideosSearch

class SBRemoteCache():
    def __init__ (self, fn="vidcache.json", debug = False):
        self.filename = fn
        self.cache = {}
        self.load_cache()
        self.debug = debug
        self.sbclient = sb.Client()
        self.max_age = 43200
 
    def search(self, arg):
        if self.debug:
            print (f"New search: Looking up YT data for video \"{arg}\" ")
        videosSearch = VideosSearch(arg, limit = 2)
        return videosSearch.result()['result'][0]


    def load_cache(self):
        if os.path.exists(self.filename):
            self.cache = json.load(open(self.filename))
        else:
            self.cache = {"titles": {}, "segments": {}, "fresh": {}}
            self.save_cache()
        if "fresh" not in self.cache.keys():
            self.cache["fresh"] = {}

    def save_cache(self):
        json.dump(self.cache, open(self.filename, "w"))
    
    def remove_id_from_fresh(self, id, defer_save=False):
        nfresh = {}
        ofresh = self.cache["fresh"]
        fnd = False
        for k in ofresh:
            if id != k:
                nfresh[id] = ofresh[id]
            else:
                fnd = True
        
        if not defer_save:
            self.save_cache()
        
        return fnd
        


    def remove_id_from_segments(self, id, defer_save=False):
        sfnd = False
        new_segments = {}
        segments = self.cache["segments"]
        for vid in segments:
            obj = segments[vid]
            if vid == id:
                sfnd = True
                print (f"Found segment entry for ID \"{id}\"")
            else:
                new_segments[vid] = obj

        if not sfnd:
            print (f'ID "{id}" not found in segments')
        else:
            self.cache["segments"] = new_segments
            if not defer_save:
                self.save_cache()
        
        return sfnd

    def remove_id_from_titles(self, id, defer_save=False):
        titles = self.cache["titles"]
        new_titles = {}
        tfnd = False
        for t in titles:
            obj = titles[t]
            if obj["id"] == id:
                tfnd = True
                print (f"Found title entry for ID \"{id}\"")
            else:
                new_titles[t] = obj

        if not tfnd:
            print (f'ID "{id}" not found in titles')
        else:
            self.cache["titles"] = new_titles
            if not defer_save:
                self.save_cache()
        
        return tfnd
        
    def remove_id_from_cache(self, id):
        sfnd = self.remove_id_from_segments(id, True)
        tfnd = self.remove_id_from_titles(id, True)
        ffnd = self.remove_id_from_fresh(id, True)
        if sfnd or tfnd:
            self.save_cache()


    def lookup_segments(self, id):
        url = "https://www.youtube.com/watch?v=%s" % (id)
        if self.debug:
            print (f"Looking up segments for {url}")
        result = []
        try:
            skip_segments = self.sbclient.get_skip_segments(url)
            result = [ x.data for x in skip_segments ]
        except (sb.errors.NotFoundException, sb.errors.InvalidJSONException) as ex:
            if self.debug:
                print (f"Error: {ex}")
            print ("Video ID not found")
        return result

    def segments_are_old (self, id):
        fsegments = self.cache["fresh"]
        if id in fsegments.keys():
            diff = time.time() - fsegments[id]
            if diff > self.max_age:
                return True
            else:
                return False
        return True

    def lookup_video (self, artist, title):
        titles = self.cache["titles"]
        segments = self.cache["segments"]
        hl = f"{artist} {title}"
        need_save_cache = False
        if hl not in titles.keys():
            video = self.search(hl)
            obj = {"id": video["id"], "artist": artist, "title": title }
            self.cache["titles"][hl] = obj
            need_save_cache = True
        else:
            video = titles[hl]
        
        id = video["id"]
        fnd_segments = id in segments.keys()
        segments_old = self.segments_are_old(id)
        #print (f"Segments old: {segments_old}")


        if not fnd_segments or segments_old:
            skip_segments = self.lookup_segments(id)
            segments[id] = skip_segments
            self.cache["fresh"][id] = time.time()
            self.cache["segments"] = segments
            need_save_cache = True
        else:
            skip_segments = segments[id]
        
        if need_save_cache:
            self.save_cache()
        
        r = {"video": self.cache["titles"][hl], "segments": self.cache["segments"][id] }

        return r
    
        

