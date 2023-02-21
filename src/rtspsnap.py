import argparse
import datetime
import os
import tempfile

import cv2


if __name__ == '__main__':

    description = "Save off a snapshot of an RTSP camera stream"
    parser = argparse.ArgumentParser(usage=None, description=description)

    parser.add_argument("-a",
                        "--auth",
                        type=str,
                        required=False,
                        help="<username>:<password>")

    parser.add_argument("-s",
                        "--stream-address",
                        type=str,
                        required=True,
                        help="RTSP Stream URL ex. 'rtsp://hostname:port/stream/path")

    parser.add_argument("-d",
                        "--directory",
                        type=str,
                        required=False,
                        default=tempfile.gettempdir(),
                        help="Directory to store snapshot in.")

    parser.add_argument("-t",
                        "--timestamp",
                        action="store_true",
                        default=False,
                        help="Tag snapshot with timestamp.")

    parser.add_argument("-v",
                        "--verbose",
                        action="store_true",
                        default=False,
                        help="Print debug information.")

    args = parser.parse_args()

    savedir = args.directory
    timeflag = args.timestamp

    stream_addr = args.stream_address
    auth = args.auth


    def event_printer(e):
        if args.verbose:
            t = datetime.datetime.utcnow()
            print("{}: {}".format(t, e))
    
    event_printer("Saving Snapshots To: {}".format(savedir))
    event_printer("Connecting to stream URL: {}".format(stream_addr))

    if auth:
        username, password = auth.split(":")
        stream_addr = stream_addr.split("rtsp://")[1]
        stream_addr = "rtsp://{}:{}@{}".format(username,
                                               password,
                                               stream_addr)

    try:
        camera_capture = cv2.VideoCapture(stream_addr)
        if camera_capture.isOpened():
            ret, frame = camera_capture.read()
            capture_time = datetime.datetime.utcnow().strftime("%Y%m%d-%H.%M.%S")

            if timeflag:
                height, width, channels = frame.shape
                cv2.putText(frame,
                            f"{capture_time}",
                            (0, height-4),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            2,
                            (255,255,255),
                            3)

            #cv2.imshow('frame', frame)
            #cv2.waitKey(0)
            
            outfile = os.path.join(savedir, f"{capture_time}.jpg")
            event_printer(f" - Writing file to {outfile}")
            cv2.imwrite(outfile, frame)

            camera_capture.release()
            #cv2.destroyAllWindows()

    except Exception as ex:
        print(f"{ex}")
            
