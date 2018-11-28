# Copy of http://stackoverflow.com/a/20104705
# from threading import Thread
from flask import Flask, Blueprint, request, Response, render_template, jsonify
from flask_restplus import Api, Resource, apidoc, fields
from flask_bootstrap import Bootstrap, WebCDN
from flask_socketio import SocketIO, send
import os
# import cv2
# import sys
# import numpy


@socketio.on('message')
def handle_message(message):
    # print('Socket message: {}'.format(msg))
    # print(msg['name'])
    # send('Nice')
    context['current_job']['name'] = message['name']
    # print(context["current_job"]["name"])


#  <!-- <img src="{{ url_for('video_feed') }}" class="figure-img img-fluid rounded" alt="Camera feed"> -->
# @app.route('/video_feed')
# def video_feed():
#     return Response(get_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')


# def get_frame():

#     camera_port = 1
#     camera = cv2.VideoCapture(camera_port)  # this makes a web cam object

#     while True:
#         ret, frame = camera.read()
#         ret, jpeg = cv2.imencode('.jpg', frame)
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')
#     del(camera)

def run_job(job_name):
    import json

    file_path = JOBS_DIR + '/' + job_name + '.json'
    with open(file_path, 'r') as job_file:
        job = json.load(job_file)
        total_count = len(job['components'])
        count = 0
        for component in job['components']:
            count += 1
            progress_percent = 100 * count / total_count
            print(progress_percent)
            print(component)


if __name__ == '__main__':
    try:
        # machine.open()
        # app.run(host='0.0.0.0', debug=True, extra_files=get_extra_files())
        socketio.run(app, host='0.0.0.0', port=5000, debug=True,
                     extra_files=get_extra_files())
    finally:
        print("Finally_app_id: ", '{}'.format(id(app)))
        # machine.close()

        # if __name__ == "__main__":
        #     from gevent import pywsgi
        #     from geventwebsocket.handler import WebSocketHandler
        #     server = pywsgi.WSGIServer(('', 6000), app, handler_class=WebSocketHandler)
        #     server.serve_forever()

        # class WebcamVideoStream:
        #     def __init__(self, src=0):
        #         # initialize the video camera stream and read the first frame
        #         # from the stream
        #         self.stream = cv2.VideoCapture(src)
        #         (self.grabbed, self.frame) = self.stream.read()

        #         # initialize the variable used to indicate if the thread should
        #         # be stopped
        #         self.stopped = False

        #     def start(self):
        #         # start the thread to read frames from the video stream
        #         Thread(target=self.update, args=()).start()
        #         return self

        #     def update(self):
        #         # keep looping infinitely until the thread is stopped
        #         while True:
        #             # if the thread indicator variable is set, stop the thread
        #             if self.stopped:
        #                 return

        #             # otherwise, read the next frame from the stream
        #             (self.grabbed, self.frame) = self.stream.read()

        #     def read(self):
        #         # return the frame most recently read
        #         return self.frame

        #     def stop(self):
        #         # indicate that the thread should be stopped
        #         self.stopped = True
