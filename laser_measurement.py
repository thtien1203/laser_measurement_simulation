#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: laser_measurement
# GNU Radio version: 3.10.9.2

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from gnuradio import analog
from gnuradio import blocks
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import sip



class laser_measurement(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "laser_measurement", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("laser_measurement")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "laser_measurement")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.distance = distance = 4921.26
        self.speedOfLight_c = speedOfLight_c = 3*10**8
        self.samp_rate = samp_rate = 10**7
        self.distance_ft = distance_ft = distance/3.28084
        self.delay_samples = delay_samples = int((2*distance_ft/speedOfLight_c)*samp_rate)

        ##################################################
        # Blocks
        ##################################################

        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
            1024, #size
            samp_rate, #samp_rate
            "Laser Signal Time", #name
            3, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_NORM, qtgui.TRIG_SLOPE_POS, 0.5, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(3):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.measured_distance = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
            1,
            None # parent
        )
        self.measured_distance.set_update_time(0.10)
        self.measured_distance.set_title("Measured Distance (ft)")

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        units = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(1):
            self.measured_distance.set_min(i, -1)
            self.measured_distance.set_max(i, 1)
            self.measured_distance.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.measured_distance.set_label(i, "Data {0}".format(i))
            else:
                self.measured_distance.set_label(i, labels[i])
            self.measured_distance.set_unit(i, units[i])
            self.measured_distance.set_factor(i, factor[i])

        self.measured_distance.enable_autoscale(False)
        self._measured_distance_win = sip.wrapinstance(self.measured_distance.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._measured_distance_win)
        self.fir_filter_xxx_0 = filter.fir_filter_fff(1, [1,1,1,1,1])
        self.fir_filter_xxx_0.declare_sample_delay(0)
        self._distance_range = qtgui.Range(0, 16404, 49.2126, 4921.26, 200)
        self._distance_win = qtgui.RangeWidget(self._distance_range, self.set_distance, "Distance (ft)", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._distance_win)
        self.blocks_vector_source_x_0 = blocks.vector_source_f([1]*5+[0]*995, True, 1, [])
        self.blocks_throttle2_0 = blocks.throttle( gr.sizeof_float*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_float*1, 1000)
        self.blocks_short_to_float_0 = blocks.short_to_float(1, 1)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_short*1)
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_ff((speedOfLight_c/(2*samp_rate)*3.28084))
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff((min(1, 0.1*(1500/max(distance_ft,15))**2)))
        self.blocks_delay_0 = blocks.delay(gr.sizeof_float*1, delay_samples)
        self.blocks_argmax_xx_0 = blocks.argmax_fs(1000)
        self.blocks_add_xx_0 = blocks.add_vff(1)
        self.blocks_add_const_vxx_0 = blocks.add_const_ff((-4))
        self.analog_noise_source_x_0 = analog.noise_source_f(analog.GR_GAUSSIAN, 0.01, 0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_noise_source_x_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.blocks_multiply_const_vxx_1, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.fir_filter_xxx_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.qtgui_time_sink_x_0, 1))
        self.connect((self.blocks_argmax_xx_0, 1), (self.blocks_null_sink_0, 0))
        self.connect((self.blocks_argmax_xx_0, 0), (self.blocks_short_to_float_0, 0))
        self.connect((self.blocks_delay_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.measured_distance, 0))
        self.connect((self.blocks_short_to_float_0, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.blocks_argmax_xx_0, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.blocks_delay_0, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.blocks_vector_source_x_0, 0), (self.blocks_throttle2_0, 0))
        self.connect((self.fir_filter_xxx_0, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.fir_filter_xxx_0, 0), (self.qtgui_time_sink_x_0, 2))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "laser_measurement")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_distance(self):
        return self.distance

    def set_distance(self, distance):
        self.distance = distance
        self.set_distance_ft(self.distance/3.28084)

    def get_speedOfLight_c(self):
        return self.speedOfLight_c

    def set_speedOfLight_c(self, speedOfLight_c):
        self.speedOfLight_c = speedOfLight_c
        self.set_delay_samples(int((2*self.distance_ft/self.speedOfLight_c)*self.samp_rate))
        self.blocks_multiply_const_vxx_1.set_k((self.speedOfLight_c/(2*self.samp_rate)*3.28084))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_delay_samples(int((2*self.distance_ft/self.speedOfLight_c)*self.samp_rate))
        self.blocks_multiply_const_vxx_1.set_k((self.speedOfLight_c/(2*self.samp_rate)*3.28084))
        self.blocks_throttle2_0.set_sample_rate(self.samp_rate)
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)

    def get_distance_ft(self):
        return self.distance_ft

    def set_distance_ft(self, distance_ft):
        self.distance_ft = distance_ft
        self.set_delay_samples(int((2*self.distance_ft/self.speedOfLight_c)*self.samp_rate))
        self.blocks_multiply_const_vxx_0.set_k((min(1, 0.1*(1500/max(self.distance_ft,15))**2)))

    def get_delay_samples(self):
        return self.delay_samples

    def set_delay_samples(self, delay_samples):
        self.delay_samples = delay_samples
        self.blocks_delay_0.set_dly(int(self.delay_samples))




def main(top_block_cls=laser_measurement, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
