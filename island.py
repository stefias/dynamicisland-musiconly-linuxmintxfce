import sys
import os
import urllib.parse
import urllib.request
import random
import dbus
import faulthandler

from PyQt5.QtCore import (
    Qt,
    QPropertyAnimation,
    QRect,
    QRectF,
    QEasingCurve,
    QTimer,
    QSize,
    QParallelAnimationGroup,
    pyqtProperty,
)

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QGraphicsOpacityEffect,
)

from PyQt5.QtGui import (
    QPainter,
    QColor,
    QPixmap,
    QImage,
    QFont,
    QPainterPath,
    QLinearGradient,
    QPen,
)

faulthandler.enable()


# ============================================================
# ANIMATED WAVEFORM
# ============================================================

class AnimatedWaveform(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate_bars)

        self.heights = [6, 12, 18, 9, 15]
        self.target_heights = [6, 12, 18, 9, 15]

        self.is_playing = False

        self.color1 = QColor(220, 150, 240)
        self.color2 = QColor(140, 70, 160)

        self.setAttribute(
            Qt.WA_TranslucentBackground,
            True
        )

    def set_colors(self, c1, c2):
        self.color1 = c1
        self.color2 = c2
        self.update()

    def start_animation(self):
        self.is_playing = True

        if not self.timer.isActive():
            self.timer.start(50)

    def stop_animation(self):
        self.is_playing = False
        self.timer.stop()

        self.target_heights = [5, 5, 5, 5, 5]
        self.update()

    def animate_bars(self):

        if self.is_playing:
            self.target_heights = [
                random.randint(5, 24)
                for _ in range(5)
            ]

        for i in range(len(self.heights)):

            difference = (
                self.target_heights[i]
                - self.heights[i]
            )

            if abs(difference) < 1:
                self.heights[i] = self.target_heights[i]
            else:
                self.heights[i] += difference * 0.25

        self.update()

    def paintEvent(self, event):

        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.Antialiasing
        )

        painter.setPen(Qt.NoPen)

        gradient = QLinearGradient(
            0,
            0,
            0,
            self.height()
        )

        gradient.setColorAt(
            0.0,
            self.color1
        )

        gradient.setColorAt(
            1.0,
            self.color2
        )

        painter.setBrush(gradient)

        bar_width = 3
        spacing = 3

        for i, height in enumerate(self.heights):

            h = max(
                3,
                int(height)
            )

            x = i * (
                bar_width
                + spacing
            )

            y = (
                self.height()
                - h
            ) // 2

            painter.drawRoundedRect(
                x,
                y,
                bar_width,
                h,
                1.5,
                1.5
            )


# ============================================================
# ALBUM ART
# ============================================================

class AlbumArtWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.cached_pixmap = None
        self.radius = 6

        self.setAttribute(
            Qt.WA_TranslucentBackground,
            True
        )

    def set_pixmap(self, pixmap):

        self.cached_pixmap = pixmap
        self.update()

    def set_radius(self, radius):

        self.radius = int(radius)
        self.update()

    def paintEvent(self, event):

        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.Antialiasing,
            True
        )

        painter.setRenderHint(
            QPainter.SmoothPixmapTransform,
            True
        )

        if self.width() <= 0 or self.height() <= 0:
            return

        path = QPainterPath()

        path.addRoundedRect(
            QRectF(
                0,
                0,
                self.width(),
                self.height()
            ),
            self.radius,
            self.radius
        )

        painter.setClipPath(path)

        if (
            not self.cached_pixmap
            or self.cached_pixmap.isNull()
        ):

            painter.fillRect(
                self.rect(),
                QColor(30, 30, 30)
            )

            painter.end()
            return

        size = min(
            self.width(),
            self.height()
        )

        scaled = self.cached_pixmap.scaled(
            QSize(
                size,
                size
            ),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )

        x = (
            self.width()
            - scaled.width()
        ) // 2

        y = (
            self.height()
            - scaled.height()
        ) // 2

        painter.drawPixmap(
            x,
            y,
            scaled
        )

        painter.end()


# ============================================================
# ICON BUTTON
# ============================================================

class IconButton(QPushButton):

    def __init__(
        self,
        icon_type,
        parent=None
    ):

        super().__init__(parent)

        self.icon_type = icon_type

        self.setCursor(
            Qt.PointingHandCursor
        )

        self.setFlat(True)

        self.setStyleSheet(
            "background: transparent;"
            "border: none;"
        )

    def paintEvent(self, event):

        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.Antialiasing
        )

        color = (
            QColor(190, 190, 190)
            if self.isDown()
            or self.underMouse()
            else QColor(255, 255, 255)
        )

        painter.setBrush(color)
        painter.setPen(Qt.NoPen)

        w = self.width()
        h = self.height()

        def draw_rounded_tri(
            x,
            y,
            width,
            height,
            right=True
        ):

            path = QPainterPath()

            if right:

                path.moveTo(
                    x,
                    y
                )

                path.lineTo(
                    x + width,
                    y + height / 2
                )

                path.lineTo(
                    x,
                    y + height
                )

            else:

                path.moveTo(
                    x + width,
                    y
                )

                path.lineTo(
                    x,
                    y + height / 2
                )

                path.lineTo(
                    x + width,
                    y + height
                )

            path.closeSubpath()

            painter.setPen(
                QPen(
                    color,
                    4,
                    Qt.SolidLine,
                    Qt.RoundCap,
                    Qt.RoundJoin
                )
            )

            painter.drawPath(path)

            painter.setPen(Qt.NoPen)

            painter.drawPath(path)

        if self.icon_type == "play":

            draw_rounded_tri(
                w * 0.25,
                h * 0.1,
                w * 0.58,
                h * 0.75,
                True
            )

        elif self.icon_type == "pause":

            bw = w * 0.3
            bh = h * 0.75

            painter.drawRoundedRect(
                int(w * 0.15),
                int((h - bh) / 2),
                int(bw),
                int(bh),
                3,
                3
            )

            painter.drawRoundedRect(
                int(w * 0.55),
                int((h - bh) / 2),
                int(bw),
                int(bh),
                3,
                3
            )

        elif self.icon_type == "next":

            tw = w * 0.42
            th = h * 0.6

            draw_rounded_tri(
                w * 0.05,
                (h - th) / 2,
                tw,
                th,
                True
            )

            draw_rounded_tri(
                w * 0.5,
                (h - th) / 2,
                tw,
                th,
                True
            )

        elif self.icon_type == "prev":

            tw = w * 0.42
            th = h * 0.6

            draw_rounded_tri(
                w * 0.08,
                (h - th) / 2,
                tw,
                th,
                False
            )

            draw_rounded_tri(
                w * 0.53,
                (h - th) / 2,
                tw,
                th,
                False
            )


# ============================================================
# DYNAMIC ISLAND
# ============================================================

class SimpleDynamicIsland(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowFlags(
            Qt.FramelessWindowHint
            | Qt.WindowStaysOnTopHint
            | Qt.Tool
        )

        self.setAttribute(
            Qt.WA_TranslucentBackground,
            True
        )

        # ----------------------------------------------------
        # SIZE
        # ----------------------------------------------------

        self.margin = 16

        self.base_collapsed_w = 240
        self.base_collapsed_h = 42

        self.base_expanded_w = 400
        self.base_expanded_h = 200

        self.collapsed_w = (
            self.base_collapsed_w
            + self.margin * 2
        )

        self.collapsed_h = (
            self.base_collapsed_h
            + self.margin * 2
        )

        self.expanded_w = (
            self.base_expanded_w
            + self.margin * 2
        )

        self.expanded_h = (
            self.base_expanded_h
            + self.margin * 2
        )

        self.y_pos = 12

        screen = QApplication.primaryScreen().geometry()

        self.screen_width = screen.width()

        self.x_pos = (
            self.screen_width
            - self.collapsed_w
        ) // 2

        self.setGeometry(
            self.x_pos,
            self.y_pos,
            self.collapsed_w,
            self.collapsed_h
        )

        # ----------------------------------------------------
        # DBUS
        # ----------------------------------------------------

        try:

            self.bus = dbus.SessionBus()

        except Exception as e:

            print(
                f"DBus Error: {e}"
            )

            self.bus = None

        self.mpris_player = None

        # ----------------------------------------------------
        # STATE
        # ----------------------------------------------------

        self.is_expanded = False
        self.is_animating = False

        self._morph = 0.0

        self.track_id = ""

        self.track_title = "Entropy"
        self.track_artist = "Beach Bunny"

        self.art_url = ""

        self.art_request_id = 0

        self.track_length = 0

        # Actual MPRIS position in seconds.
        # Float is used so the progress bar moves smoothly.
        self.current_position = 0
        self.current_position_float = 0.0

        self.cached_pixmap = None

        self.is_playing = False

        # ----------------------------------------------------
        # UI
        # ----------------------------------------------------

        self.setup_ui()

        self.setup_animation()

        # ----------------------------------------------------
        # TIMERS
        # ----------------------------------------------------

        self.smooth_timer = QTimer(self)

        self.smooth_timer.timeout.connect(
            self.smooth_tick
        )

        # 100 ms gives smooth playback progression.
        self.smooth_timer.start(100)

        self.poll_timer = QTimer(self)

        self.poll_timer.timeout.connect(
            self.poll_media
        )

        # MPRIS is synchronized every second.
        self.poll_timer.start(1000)

        self.poll_media()

    # ========================================================
    # MORPH
    # ========================================================

    def get_morph(self):

        return self._morph

    def set_morph(self, value):

        self._morph = float(value)

        self.update_animated_content()

        self.update_artwork()

        self.update()

    morph = pyqtProperty(
        float,
        fget=get_morph,
        fset=set_morph
    )

    # ========================================================
    # UI SETUP
    # ========================================================

    def setup_ui(self):

        self.art_label = AlbumArtWidget(
            self
        )

        self.art_label.hide()

        self.title_label = QLabel(
            self.track_title,
            self
        )

        self.title_label.hide()

        self.artist_label = QLabel(
            self.track_artist,
            self
        )

        self.artist_label.hide()

        self.wave_widget = AnimatedWaveform(
            self
        )

        font_time = QFont(
            "Segoe UI",
            9,
            QFont.Medium
        )

        font_time.setStyleStrategy(
            QFont.PreferAntialias
        )

        self.time_left = QLabel(
            "0:00",
            self
        )

        self.time_left.setFont(
            font_time
        )

        self.time_left.setStyleSheet(
            "color: #e0e0e0;"
        )

        self.time_left.hide()

        self.time_right = QLabel(
            "-0:00",
            self
        )

        self.time_right.setFont(
            font_time
        )

        self.time_right.setStyleSheet(
            "color: #e0e0e0;"
        )

        self.time_right.setAlignment(
            Qt.AlignRight
            | Qt.AlignVCenter
        )

        self.time_right.hide()

        self.btn_prev = IconButton(
            "prev",
            self
        )

        self.btn_play = IconButton(
            "play",
            self
        )

        self.btn_next = IconButton(
            "next",
            self
        )

        for btn in [
            self.btn_prev,
            self.btn_play,
            self.btn_next
        ]:

            btn.hide()

            btn.clicked.connect(
                self.handle_media_button
            )

        # ----------------------------------------------------
        # OPACITY EFFECTS
        # ----------------------------------------------------

        self.opacity_widgets = [
            self.title_label,
            self.artist_label,
            self.time_left,
            self.time_right,
            self.btn_prev,
            self.btn_play,
            self.btn_next,
        ]

        self.opacity_effects = {}

        for widget in self.opacity_widgets:

            effect = QGraphicsOpacityEffect(
                widget
            )

            effect.setOpacity(0.0)

            widget.setGraphicsEffect(
                effect
            )

            self.opacity_effects[
                widget
            ] = effect

    # ========================================================
    # ANIMATION SETUP
    # ========================================================

    def setup_animation(self):

        self.animation_group = (
            QParallelAnimationGroup(self)
        )

        self.geometry_animation = (
            QPropertyAnimation(
                self,
                b"geometry"
            )
        )

        self.geometry_animation.setDuration(
            750
        )

        self.geometry_animation.setEasingCurve(
            QEasingCurve.OutExpo
        )

        self.animation_group.addAnimation(
            self.geometry_animation
        )

        self.morph_animation = (
            QPropertyAnimation(
                self,
                b"morph"
            )
        )

        self.morph_animation.setDuration(
            750
        )

        self.morph_animation.setEasingCurve(
            QEasingCurve.OutExpo
        )

        self.animation_group.addAnimation(
            self.morph_animation
        )

        self.animation_group.finished.connect(
            self.on_animation_finished
        )

    # ========================================================
    # GEOMETRIES
    # ========================================================

    def collapsed_art_geometry(self):

        return QRect(
            self.margin + 12,
            self.margin + 8,
            26,
            26
        )

    def expanded_art_geometry(self):

        return QRect(
            self.margin + 20,
            self.margin + 20,
            76,
            76
        )

    def collapsed_wave_geometry(self):

        return QRect(
            self.collapsed_w
            - self.margin
            - 42,
            self.margin + 8,
            30,
            26
        )

    def expanded_wave_geometry(self):

        return QRect(
            self.expanded_w
            - self.margin
            - 55,
            self.margin + 35,
            35,
            25
        )

    def expanded_title_geometry(self):

        return QRect(
            self.margin + 115,
            self.margin + 32,
            200,
            24
        )

    def expanded_artist_geometry(self):

        return QRect(
            self.margin + 115,
            self.margin + 58,
            200,
            24
        )

    def expanded_time_left_geometry(self):

        return QRect(
            self.margin + 25,
            self.margin + 120,
            45,
            20
        )

    def expanded_time_right_geometry(self):

        return QRect(
            self.expanded_w
            - self.margin
            - 70,
            self.margin + 120,
            45,
            20
        )

    def expanded_prev_geometry(self):

        return QRect(
            self.margin + 107,
            self.margin + 150,
            44,
            28
        )

    def expanded_play_geometry(self):

        return QRect(
            self.margin + 180,
            self.margin + 144,
            40,
            40
        )

    def expanded_next_geometry(self):

        return QRect(
            self.margin + 253,
            self.margin + 150,
            44,
            28
        )

    # ========================================================
    # ANIMATED CONTENT
    # ========================================================

    def update_animated_content(self):

        t = max(
            0.0,
            min(
                1.0,
                self._morph
            )
        )

        movement_t = (
            1.0
            - pow(
                1.0 - t,
                3
            )
        )

        def lerp(a, b, amount):

            return a + (
                b - a
            ) * amount

        def lerp_rect(
            r1,
            r2,
            amount
        ):

            return QRect(
                int(
                    lerp(
                        r1.x(),
                        r2.x(),
                        amount
                    )
                ),
                int(
                    lerp(
                        r1.y(),
                        r2.y(),
                        amount
                    )
                ),
                int(
                    lerp(
                        r1.width(),
                        r2.width(),
                        amount
                    )
                ),
                int(
                    lerp(
                        r1.height(),
                        r2.height(),
                        amount
                    )
                )
            )

        # ----------------------------------------------------
        # ALBUM ART
        # ----------------------------------------------------

        self.art_label.setGeometry(
            lerp_rect(
                self.collapsed_art_geometry(),
                self.expanded_art_geometry(),
                t
            )
        )

        # ----------------------------------------------------
        # WAVEFORM
        # ----------------------------------------------------

        self.wave_widget.setGeometry(
            lerp_rect(
                self.collapsed_wave_geometry(),
                self.expanded_wave_geometry(),
                t
            )
        )

        # ----------------------------------------------------
        # TITLE
        # ----------------------------------------------------

        title_start = QRect(
            self.margin + 115,
            self.margin + 12,
            200,
            24
        )

        self.title_label.setGeometry(
            lerp_rect(
                title_start,
                self.expanded_title_geometry(),
                movement_t
            )
        )

        # ----------------------------------------------------
        # ARTIST
        # ----------------------------------------------------

        artist_start = QRect(
            self.margin + 115,
            self.margin + 38,
            200,
            24
        )

        self.artist_label.setGeometry(
            lerp_rect(
                artist_start,
                self.expanded_artist_geometry(),
                movement_t
            )
        )

        # ----------------------------------------------------
        # TIME LEFT
        # ----------------------------------------------------

        time_left_start = QRect(
            self.margin + 25,
            self.margin + 105,
            45,
            20
        )

        self.time_left.setGeometry(
            lerp_rect(
                time_left_start,
                self.expanded_time_left_geometry(),
                movement_t
            )
        )

        # ----------------------------------------------------
        # TIME RIGHT
        # ----------------------------------------------------

        time_right_start = QRect(
            self.expanded_w
            - self.margin
            - 70,
            self.margin + 105,
            45,
            20
        )

        self.time_right.setGeometry(
            lerp_rect(
                time_right_start,
                self.expanded_time_right_geometry(),
                movement_t
            )
        )

        # ----------------------------------------------------
        # PREVIOUS
        # ----------------------------------------------------

        prev_start = QRect(
            self.margin + 107,
            self.margin + 130,
            44,
            28
        )

        self.btn_prev.setGeometry(
            lerp_rect(
                prev_start,
                self.expanded_prev_geometry(),
                movement_t
            )
        )

        # ----------------------------------------------------
        # PLAY
        # ----------------------------------------------------

        play_start = QRect(
            self.margin + 180,
            self.margin + 124,
            40,
            40
        )

        self.btn_play.setGeometry(
            lerp_rect(
                play_start,
                self.expanded_play_geometry(),
                movement_t
            )
        )

        # ----------------------------------------------------
        # NEXT
        # ----------------------------------------------------

        next_start = QRect(
            self.margin + 253,
            self.margin + 130,
            44,
            28
        )

        self.btn_next.setGeometry(
            lerp_rect(
                next_start,
                self.expanded_next_geometry(),
                movement_t
            )
        )

        # ----------------------------------------------------
        # OPACITY
        # ----------------------------------------------------

        for widget, effect in self.opacity_effects.items():

            effect.setOpacity(
                t
            )

        self.update()

    # ========================================================
    # SMOOTH POSITION
    # ========================================================

    def smooth_tick(self):

        if not self.is_playing:
            return

        if self.track_length <= 0:
            return

        # Advance the local position smoothly between
        # the one-second MPRIS synchronization updates.
        self.current_position_float += 0.1

        if (
            self.current_position_float
            >= self.track_length
        ):

            self.current_position_float = float(
                self.track_length
            )

            self.current_position = (
                self.track_length
            )

            self.update_progress_ui()

            return

        self.current_position = int(
            self.current_position_float
        )

        self.update_progress_ui()

    # ========================================================
    # MPRIS
    # ========================================================

    def poll_media(self):

        if not self.bus:
            return

        try:

            services = [
                s
                for s in self.bus.list_names()
                if s.startswith(
                    "org.mpris.MediaPlayer2."
                )
            ]

            if not services:
                return

            selected_service = None

            for service in services:

                try:

                    proxy = self.bus.get_object(
                        service,
                        "/org/mpris/MediaPlayer2"
                    )

                    props = dbus.Interface(
                        proxy,
                        "org.freedesktop.DBus.Properties"
                    )

                    status = str(
                        props.Get(
                            "org.mpris.MediaPlayer2.Player",
                            "PlaybackStatus"
                        )
                    )

                    if status == "Playing":

                        selected_service = service
                        break

                except Exception:

                    continue

            if selected_service is None:

                selected_service = services[0]

            player_proxy = self.bus.get_object(
                selected_service,
                "/org/mpris/MediaPlayer2"
            )

            props = dbus.Interface(
                player_proxy,
                "org.freedesktop.DBus.Properties"
            )

            self.mpris_player = dbus.Interface(
                player_proxy,
                "org.mpris.MediaPlayer2.Player"
            )

            metadata = props.Get(
                "org.mpris.MediaPlayer2.Player",
                "Metadata"
            )

            new_track_id = str(
                metadata.get(
                    "mpris:trackid",
                    ""
                )
            )

            new_title = str(
                metadata.get(
                    "xesam:title",
                    "Unknown"
                )
            )

            artists = metadata.get(
                "xesam:artist",
                ["Unknown"]
            )

            new_artist = (
                str(artists[0])
                if artists
                else "Unknown"
            )

            new_art = str(
                metadata.get(
                    "mpris:artUrl",
                    ""
                )
            )

            new_track_length = (
                int(
                    metadata.get(
                        "mpris:length",
                        0
                    )
                )
                // 1000000
            )

            # ------------------------------------------------
            # POSITION
            # ------------------------------------------------

            try:

                pos_sec = (
                    int(
                        props.Get(
                            "org.mpris.MediaPlayer2.Player",
                            "Position"
                        )
                    )
                    / 1000000.0
                )

                # MPRIS is authoritative. If our smooth
                # local timer has drifted noticeably, snap
                # back to the real player position.
                if abs(
                    pos_sec
                    - self.current_position_float
                ) > 1.0:

                    self.current_position_float = (
                        pos_sec
                    )

                else:

                    # Keep the smooth value but prevent it
                    # from exceeding the actual MPRIS value
                    # by too much.
                    if pos_sec >= 0:
                        self.current_position_float = (
                            pos_sec
                            if not self.is_playing
                            else self.current_position_float
                        )

                self.current_position = int(
                    self.current_position_float
                )

            except Exception:

                pass

            # ------------------------------------------------
            # TRACK LENGTH
            # ------------------------------------------------

            self.track_length = max(
                0,
                new_track_length
            )

            # If the track changed, use the exact MPRIS
            # position immediately instead of carrying over
            # the previous track's position.
            track_changed = (
                new_track_id
                != self.track_id
            )

            if track_changed:

                try:

                    exact_position = (
                        int(
                            props.Get(
                                "org.mpris.MediaPlayer2.Player",
                                "Position"
                            )
                        )
                        / 1000000.0
                    )

                    self.current_position_float = (
                        max(
                            0.0,
                            exact_position
                        )
                    )

                    self.current_position = int(
                        self.current_position_float
                    )

                except Exception:

                    self.current_position_float = 0.0
                    self.current_position = 0

            # ------------------------------------------------
            # PLAYBACK STATUS
            # ------------------------------------------------

            status = str(
                props.Get(
                    "org.mpris.MediaPlayer2.Player",
                    "PlaybackStatus"
                )
            )

            playing = (
                status == "Playing"
            )

            if playing != self.is_playing:

                self.is_playing = playing

                self.btn_play.icon_type = (
                    "pause"
                    if playing
                    else "play"
                )

                self.btn_play.update()

                if playing:

                    self.wave_widget.start_animation()

                else:

                    self.wave_widget.stop_animation()

            # ------------------------------------------------
            # TRACK INFORMATION
            # ------------------------------------------------

            if (
                track_changed
                or new_title != self.track_title
                or new_artist != self.track_artist
            ):

                self.track_id = new_track_id

                self.track_title = new_title

                self.track_artist = new_artist

                self.title_label.setText(
                    self.track_title
                )

                self.artist_label.setText(
                    self.track_artist
                )

            # ------------------------------------------------
            # ALBUM ART
            # ------------------------------------------------

            if (
                track_changed
                or (
                    new_art
                    and new_art != self.art_url
                )
            ):

                self.art_url = new_art

                self.art_request_id += 1

                self.load_album_art(
                    self.art_request_id
                )

            elif (
                not new_art
                and track_changed
            ):

                self.art_url = ""

                self.cached_pixmap = None

                self.art_label.set_pixmap(
                    None
                )

                self.wave_widget.set_colors(
                    QColor(220, 150, 240),
                    QColor(140, 70, 160)
                )

            # Keep position inside valid track range.
            if self.track_length > 0:

                self.current_position_float = max(
                    0.0,
                    min(
                        self.current_position_float,
                        float(self.track_length)
                    )
                )

                self.current_position = int(
                    self.current_position_float
                )

            self.update_progress_ui()

        except Exception as e:

            print(
                f"[Error in poll_media]: {e}"
            )

    # ========================================================
    # ALBUM ART
    # ========================================================

    def load_album_art(
        self,
        req_id
    ):

        try:

            if not self.art_url:

                self.cached_pixmap = None

                self.art_label.set_pixmap(
                    None
                )

                return

            loaded_pixmap = None

            if self.art_url.startswith(
                "file://"
            ):

                path = urllib.parse.unquote(
                    self.art_url[7:]
                )

                img = QImage(path)

                if not img.isNull():

                    loaded_pixmap = (
                        QPixmap.fromImage(img)
                    )

            elif (
                self.art_url.startswith(
                    "http://"
                )
                or self.art_url.startswith(
                    "https://"
                )
            ):

                req = urllib.request.Request(
                    self.art_url,
                    headers={
                        "User-Agent": "Mozilla/5.0"
                    }
                )

                with urllib.request.urlopen(
                    req,
                    timeout=3
                ) as response:

                    data = response.read()

                    img = QImage()

                    if img.loadFromData(data):

                        loaded_pixmap = (
                            QPixmap.fromImage(img)
                        )

            else:

                img = QImage(
                    self.art_url
                )

                if not img.isNull():

                    loaded_pixmap = (
                        QPixmap.fromImage(img)
                    )

            if (
                req_id
                != self.art_request_id
            ):

                return

            if (
                loaded_pixmap
                and not loaded_pixmap.isNull()
            ):

                self.cached_pixmap = (
                    loaded_pixmap
                )

                self.art_label.set_pixmap(
                    loaded_pixmap
                )

                c1, c2 = (
                    self.extract_colors_from_pixmap()
                )

                self.wave_widget.set_colors(
                    c1,
                    c2
                )

            else:

                self.cached_pixmap = None

                self.art_label.set_pixmap(
                    None
                )

        except Exception as e:

            print(
                f"[Art Load Exception]: {e}"
            )

            if (
                req_id
                == self.art_request_id
            ):

                self.cached_pixmap = None

                self.art_label.set_pixmap(
                    None
                )

    # ========================================================
    # ARTWORK
    # ========================================================

    def update_artwork(self):

        if not self.art_label.isVisible():

            return

        t = max(
            0.0,
            min(
                1.0,
                self._morph
            )
        )

        radius = int(
            6
            + (
                20 - 6
            ) * t
        )

        self.art_label.set_radius(
            radius
        )

        self.art_label.update()

    # ========================================================
    # COLORS
    # ========================================================

    def extract_colors_from_pixmap(self):

        if (
            not self.cached_pixmap
            or self.cached_pixmap.isNull()
        ):

            return (
                QColor(220, 150, 240),
                QColor(140, 70, 160)
            )

        img = (
            self.cached_pixmap
            .toImage()
            .scaled(
                QSize(4, 4),
                Qt.IgnoreAspectRatio,
                Qt.SmoothTransformation
            )
        )

        return (
            img.pixelColor(1, 1),
            img.pixelColor(2, 2)
        )

    # ========================================================
    # PROGRESS
    # ========================================================

    def update_progress_ui(self):

        self.title_label.setText(
            self.track_title
        )

        self.artist_label.setText(
            self.track_artist
        )

        # ----------------------------------------------------
        # CURRENT TIME
        # ----------------------------------------------------

        position = max(
            0.0,
            min(
                self.current_position_float,
                float(self.track_length)
                if self.track_length > 0
                else 0.0
            )
        )

        current_total = int(
            position
        )

        curr_m, curr_s = divmod(
            current_total,
            60
        )

        self.time_left.setText(
            f"{curr_m}:{curr_s:02d}"
        )

        # ----------------------------------------------------
        # REMAINING TIME
        # ----------------------------------------------------

        remaining = max(
            0,
            self.track_length - current_total
        )

        rem_m, rem_s = divmod(
            remaining,
            60
        )

        self.time_right.setText(
            f"-{rem_m}:{rem_s:02d}"
        )

        self.update()

    # ========================================================
    # MEDIA BUTTONS
    # ========================================================

    def handle_media_button(self):

        try:

            sender = self.sender()

            if not self.mpris_player:

                return

            if sender == self.btn_play:

                self.mpris_player.PlayPause()

            elif sender == self.btn_next:

                self.mpris_player.Next()

            elif sender == self.btn_prev:

                self.mpris_player.Previous()

        except Exception as e:

            print(
                f"[Media Button Error]: {e}"
            )

    # ========================================================
    # PAINT
    # ========================================================

    def paintEvent(self, event):

        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.Antialiasing
        )

        painter.fillRect(
            self.rect(),
            Qt.transparent
        )

        current_w = (
            self.width()
            - self.margin * 2
        )

        current_h = (
            self.height()
            - self.margin * 2
        )

        radius = (
            21
            + (
                48 - 21
            ) * self._morph
        )

        # ----------------------------------------------------
        # SHADOW
        # ----------------------------------------------------

        for i in range(8, 0, -1):

            shadow_path = QPainterPath()

            s_rect = QRectF(
                self.margin
                - i * 1.5,

                self.margin
                - i * 1.5,

                current_w
                + i * 3.0,

                current_h
                + i * 3.0
            )

            shadow_path.addRoundedRect(
                s_rect,
                radius + i,
                radius + i
            )

            alpha = int(
                60 / i
            )

            painter.fillPath(
                shadow_path,
                QColor(
                    0,
                    0,
                    0,
                    alpha
                )
            )

        # ----------------------------------------------------
        # MAIN ISLAND
        # ----------------------------------------------------

        painter.setBrush(
            QColor(0, 0, 0)
        )

        painter.setPen(
            Qt.NoPen
        )

        painter.drawRoundedRect(
            self.margin,
            self.margin,
            current_w,
            current_h,
            radius,
            radius
        )

        # ----------------------------------------------------
        # PROGRESS BAR
        # ----------------------------------------------------

        if self.track_length > 0:

            morph = max(
                0.0,
                min(
                    1.0,
                    self._morph
                )
            )

            # The bar itself has a fixed width.
            # Only its opacity follows the expansion.
            bar_x = (
                self.margin
                + 75
            )

            bar_y = (
                self.margin
                + 127
            )

            bar_w = 250
            bar_h = 7

            # ------------------------------------------------
            # BAR BACKGROUND
            # ------------------------------------------------

            painter.setBrush(
                QColor(
                    255,
                    255,
                    255,
                    int(55 * morph)
                )
            )

            painter.drawRoundedRect(
                bar_x,
                bar_y,
                bar_w,
                bar_h,
                3.5,
                3.5
            )

            # ------------------------------------------------
            # PLAYBACK PROGRESS
            # ------------------------------------------------

            progress = (
                self.current_position_float
                / float(self.track_length)
            )

            progress = max(
                0.0,
                min(
                    1.0,
                    progress
                )
            )

            fill_w = int(
                bar_w
                * progress
            )

            if fill_w > 0:

                painter.setBrush(
                    QColor(
                        255,
                        255,
                        255,
                        int(255 * morph)
                    )
                )

                painter.drawRoundedRect(
                    bar_x,
                    bar_y,
                    fill_w,
                    bar_h,
                    3.5,
                    3.5
                )

        painter.end()

    # ========================================================
    # MOUSE / EXPANSION
    # ========================================================

    def mousePressEvent(self, event):

        if self.is_animating:

            return

        if event.button() != Qt.LeftButton:

            return

        self.is_animating = True

        self.animation_group.stop()

        current_geo = self.geometry()

        expanding = (
            not self.is_expanded
        )

        self.is_expanded = expanding

        if expanding:

            target_w = self.expanded_w
            target_h = self.expanded_h

            start_morph = self._morph
            end_morph = 1.0

            target_x = (
                self.screen_width
                - target_w
            ) // 2

            self.prepare_expanded_ui()

        else:

            target_w = self.collapsed_w
            target_h = self.collapsed_h

            start_morph = self._morph
            end_morph = 0.0

            target_x = (
                self.screen_width
                - target_w
            ) // 2

            self.prepare_collapsed_ui()

        target_rect = QRect(
            target_x,
            self.y_pos,
            target_w,
            target_h
        )

        self.geometry_animation.setStartValue(
            current_geo
        )

        self.geometry_animation.setEndValue(
            target_rect
        )

        self.morph_animation.setStartValue(
            start_morph
        )

        self.morph_animation.setEndValue(
            end_morph
        )

        self.animation_group.start()

    # ========================================================
    # PREPARE EXPANDED
    # ========================================================

    def prepare_expanded_ui(self):

        self.art_label.show()
        self.wave_widget.show()

        for widget in self.opacity_widgets:

            widget.show()

        font_t = QFont(
            "Segoe UI",
            13,
            QFont.Bold
        )

        font_t.setStyleStrategy(
            QFont.PreferAntialias
        )

        self.title_label.setFont(
            font_t
        )

        self.title_label.setStyleSheet(
            "color: white;"
        )

        font_a = QFont(
            "Segoe UI",
            12
        )

        font_a.setStyleStrategy(
            QFont.PreferAntialias
        )

        self.artist_label.setFont(
            font_a
        )

        self.artist_label.setStyleSheet(
            "color: #bbbbbb;"
        )

        self.update_animated_content()

        self.update_artwork()

        self.title_label.raise_()
        self.artist_label.raise_()
        self.wave_widget.raise_()
        self.art_label.raise_()
        self.time_left.raise_()
        self.time_right.raise_()
        self.btn_prev.raise_()
        self.btn_play.raise_()
        self.btn_next.raise_()

    # ========================================================
    # PREPARE COLLAPSED
    # ========================================================

    def prepare_collapsed_ui(self):

        self.art_label.show()
        self.wave_widget.show()

        for widget in self.opacity_widgets:

            widget.show()

        self.update_animated_content()

        self.update_artwork()

    # ========================================================
    # ANIMATION FINISHED
    # ========================================================

    def on_animation_finished(self):

        if self.is_expanded:

            self.set_morph(
                1.0
            )

            for widget in self.opacity_widgets:

                widget.show()

                self.opacity_effects[
                    widget
                ].setOpacity(
                    1.0
                )

        else:

            self.set_morph(
                0.0
            )

            for widget in self.opacity_widgets:

                widget.hide()

            self.art_label.show()
            self.wave_widget.show()

            self.update_artwork()

        self.is_animating = False


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    app = QApplication(sys.argv)

    # --------------------------------------------------------
    # INITIAL COLLAPSED STATE
    # --------------------------------------------------------

    island = SimpleDynamicIsland()

    island._morph = 0.0
    island.is_expanded = False

    island.art_label.setGeometry(
        island.collapsed_art_geometry()
    )

    island.wave_widget.setGeometry(
        island.collapsed_wave_geometry()
    )

    island.art_label.show()
    island.wave_widget.show()

    for widget in island.opacity_widgets:

        widget.hide()

    island.update_artwork()

    island.show()

    sys.exit(
        app.exec_()
    )
