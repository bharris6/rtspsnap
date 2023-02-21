# rtspsnap

Take a single snapshot of an RTSP steam.

## Usage

Output is a single `jpg`-formatted image whose filename is of the form `YYYYMMDDThhmmss.jpg`.  

All times in logs, in image timestamps, and in filenames are in UTC.

### General

Given an RTSP URL of `rtsp://192.168.1.1:554/stream/stream0`,

```
$ python rtspsnap.py -s rtsp://192.168.1.1:554/stream/stream0
```

### Authentication

If you need a username and password, you either put it in the stream URL itself...

```
$ python rtspsnap.py -s rtsp://username:password@192.168.1.1:554/stream/stream0
```

...or pass them in separately:

```
$ python rtspsnap.py -s rtsp://192.168.1.1:554/stream/stream0 --auth "username:password"
```

### Storage Directory

By default, `rtspsnap.py` will use the system's temporary directory (ex. `/tmp` on most Linux machines) to store the snapshot images under.  You can provide a different base directory using the `-d`/`--directory` flag:

```
$ python rtspsnap.py -s rtsp://username:password@192.168.1.1:554/stream/stream0 -d /path/to/storage/dir
```

### Timestamping

By default, `rtspsnap.py` will *not* overlay a timestamp on the snapshot image.  You can use the `-t`/`--timestamp` flag to tell `rtspsnap.py` to write a UTC timestamp onto the snapshot image:

```
$ python rtspsnap.py -s rtsp://username:password@192.168.1.1:554/stream/stream0 -t
```
