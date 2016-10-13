'''This module provides the GUI of a track.'''
from panda3d.core import TextNode
from direct.gui.OnscreenText import OnscreenText
from racing.game.gameobject.gameobject import Gui
from racing.game.engine.gui.imgbtn import ImageButton
from direct.gui.OnscreenImage import OnscreenImage


class _Gui(Gui):
    '''This class models the GUI component of a track.'''

    def __init__(self, mdt, track):
        self.__res_txts = None
        self.corners = None
        self.__buttons = None
        self.result_img = None
        Gui.__init__(self, mdt)
        self.track = track
        self.debug_txt = OnscreenText(
            '', pos=(-.1, .1), scale=0.05, fg=(1, 1, 1, 1),
            parent=eng.base.a2dBottomRight, align=TextNode.ARight,
            font=eng.font_mgr.load_font('assets/fonts/zekton rg.ttf'))
        self.__wip_txt = OnscreenText(
            _('work in progress'), pos=(.1, .1), scale=0.05, fg=(1, 1, 1, 1),
            parent=eng.base.a2dBottomLeft, align=TextNode.ALeft,
            font=eng.font_mgr.load_font('assets/fonts/zekton rg.ttf'))
        self.__countdown_txt = OnscreenText(
            '', pos=(0, 0), scale=.2, fg=(1, 1, 1, 1),
            font=eng.font_mgr.load_font('assets/fonts/zekton rg.ttf'))
        self.__keys_img = OnscreenImage(
            image='assets/images/gui/keys.png', parent=eng.base.a2dTopLeft,
            pos=(.7, 1, -.4), scale=(.6, 1, .3))
        self.__keys_img.setTransparency(True)
        self.way_txt = OnscreenText(
            '', pos=(.1, .4), scale=0.1, fg=(1, 1, 1, 1),
            parent=eng.base.a2dBottomLeft, align=TextNode.ALeft,
            font=eng.font_mgr.load_font('assets/fonts/zekton rg.ttf'))
        self.countdown_cnt = 3
        self.minimap = OnscreenImage(
            'assets/images/minimaps/%s.jpg' % track, pos=(-.25, 1, .25),
            scale=.2, parent=eng.base.a2dBottomRight)
        self.car_handle = OnscreenImage(
            'assets/images/minimaps/car_handle.png', pos=(-.25, 1, .25),
            scale=.03, parent=eng.base.a2dBottomRight)
        self.car_handle.setTransparency(True)
        self.set_corners()
        taskMgr.doMethodLater(1.0, self.process_countdown, 'coutdown')

    def set_corners(self):
        '''Sets track's corners.'''
        corners = ['topleft', 'topright', 'bottomright', 'bottomleft']
        p_mod = self.mdt.gfx.phys_model
        corners = [p_mod.find('**/Minimap' + crn) for crn in corners]
        if not any(crn.isEmpty() for crn in corners):
            self.corners = [corner.get_pos() for corner in corners]

    def update_minimap(self):
        '''Updates the minimap.'''
        if not hasattr(self, 'corners'):
            return
        left, right = self.corners[0].getX(), self.corners[1].getX()
        top, bottom = self.corners[0].getY(), self.corners[3].getY()
        car_pos = game.player_car.gfx.nodepath.get_pos()
        pos_x_norm = (car_pos.getX() - left) / (right - left)
        pos_y_norm = (car_pos.getY() - bottom) / (top - bottom)

        width = self.minimap.getScale()[0] * 2.0
        height = self.minimap.getScale()[2] * 2.0
        center_x, center_y = self.minimap.getX(), self.minimap.getZ()
        left_img = center_x - width / 2.0
        bottom_img = center_y - height / 2.0
        pos_x = left_img + pos_x_norm * width
        pos_y = bottom_img + pos_y_norm * height
        self.car_handle.set_pos(pos_x, 1, pos_y)
        self.car_handle.setR(-game.player_car.gfx.nodepath.getH())

    def process_countdown(self, task):
        '''Processes the initial countdown.'''
        if self.countdown_cnt >= 0:
            self.mdt.audio.countdown_sfx.play()
            txt = str(self.countdown_cnt) if self.countdown_cnt else _('GO!')
            self.__countdown_txt.setText(txt)
            self.countdown_cnt -= 1
            return task.again
        else:
            self.__countdown_txt.destroy()
            destroy_keys = lambda task: self.__keys_img.destroy()
            taskMgr.doMethodLater(5.0, destroy_keys, 'destroy keys')
            game.track.fsm.demand('Race')

    def show_results(self):
        '''Shows race results.'''
        self.result_img = OnscreenImage(image='assets/images/gui/results.png',
                                        scale=(.8, 1, .8))
        self.result_img.setTransparency(True)
        laps = len(game.player_car.logic.lap_times)
        self.__res_txts = [OnscreenText(
            str(game.player_car.logic.lap_times[i-1]) if i else '',
            pos=(.3, .2 - .2 * i), scale=.1, fg=(.75, .75, .75, 1),
            font=eng.font_mgr.load_font('assets/fonts/zekton rg.ttf'))
            for i in range(laps)]
        self.__res_txts += [OnscreenText(
            _('LAP'), pos=(-.3, .35), scale=.1, fg=(.75, .75, .75, 1),
            font=eng.font_mgr.load_font('assets/fonts/zekton rg.ttf'))
            for i in range(4)]
        self.__res_txts += [OnscreenText(
            str(i), pos=(-.3, .2 - .2 * i), scale=.1, fg=(.75, .75, .75, 1),
            font=eng.font_mgr.load_font('assets/fonts/zekton rg.ttf'))
            for i in range(1, 4)]
        self.__res_txts += [OnscreenText(
            _('share:'), pos=(-.1, -.65), scale=.1, fg=(.75, .75, .75, 1),
            font=eng.font_mgr.load_font('assets/fonts/zekton rg.ttf'),
            align=TextNode.A_right)]
        self.__buttons = []

        curr_time = min(game.player_car.logic.lap_times or [0])
        facebook_url = \
            'https://www.facebook.com/sharer/sharer.php?u=ya2.it/yorg'
        #TODO: find a way to share the time on Facebook
        twitter_url = 'https://twitter.com/share?text=' + \
            'I%27ve%20achieved%20{time}%20in%20the%20{track}%20track%20on' + \
            '%20Yorg%20by%20%40ya2tech%21&hashtags=yorg'
        twitter_url = twitter_url.format(time=curr_time, track=self.track)
        plus_url = 'https://plus.google.com/share?url=ya2.it/yorg'
        #TODO: find a way to share the time on Google Plus
        tumblr_url = 'https://www.tumblr.com/widgets/share/tool?url=ya2.it'
        #TODO: find a way to share the time on Tumblr
        sites = [('facebook', facebook_url), ('twitter', twitter_url),
                 ('google_plus', plus_url), ('tumblr', tumblr_url)]
        self.__buttons += [
            ImageButton(
                scale=.1,
                pos=(.02 + i*.15, 1, -.62), frameColor=(0, 0, 0, 0),
                image='assets/images/icons/%s_png.png' % site[0],
                command=eng.gui.open_browser, extraArgs=[site[1]],
                rolloverSound=loader.loadSfx('assets/sfx/menu_over.wav'),
                clickSound=loader.loadSfx('assets/sfx/menu_clicked.ogg'))
            for i, site in enumerate(sites)]

        def step():
            '''Goes on.'''
            map(lambda txt: txt.destroy(), self.__res_txts)
            map(lambda btn: btn.destroy(), self.__buttons)
            self.result_img.destroy()
            if game.ranking:
                for car in game.ranking:
                    game.ranking[car] += game.track.race_ranking[car]
                game.options['last_ranking'] = game.ranking
                game.options.store()
                game.fsm.demand('Ranking')
            else:
                game.fsm.demand('Menu')
        taskMgr.doMethodLater(10.0, lambda tsk: step(), 'step')

    def destroy(self):
        Gui.destroy(self)
        self.__wip_txt.destroy()
        self.way_txt.destroy()
        self.minimap.destroy()
        self.car_handle.destroy()