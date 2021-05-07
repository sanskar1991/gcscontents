"""
Generic FileSystem class to be used by the Content Manager
"""
import base64
import os
import requests
import json

from tornado.web import HTTPError

from gcscontents.nbimports import HasTraits, Unicode

class GenericFS(HasTraits):
    def ls(self, path=""):
        raise NotImplementedError(
            "Should be implemented by the file system abstraction"
        )

    def isfile(self, path):
        raise NotImplementedError(
            "Should be implemented by the file system abstraction"
        )

    def isdir(self, path):
        raise NotImplementedError(
            "Should be implemented by the file system abstraction"
        )

    def mv(self, old_path, new_path):
        raise NotImplementedError(
            "Should be implemented by the file system abstraction"
        )

    def cp(self, old_path, new_path):
        raise NotImplementedError(
            "Should be implemented by the file system abstraction"
        )

    def rm(self, path):
        raise NotImplementedError(
            "Should be implemented by the file system abstraction"
        )

    def mkdir(self, path):
        raise NotImplementedError(
            "Should be implemented by the file system abstraction"
        )

    def read(self, path, format):
        raise NotImplementedError(
            "Should be implemented by the file system abstraction"
        )

    def lstat(self, path):
        raise NotImplementedError(
            "Should be implemented by the file system abstraction"
        )

    def write(self, path, content, format):
        raise NotImplementedError(
            "Should be implemented by the file system abstraction"
        )


class GenericFSError(Exception):
    pass


class NoSuchFile(GenericFSError):
    def __init__(self, path, *args, **kwargs):
        self.path = path
        self.message = "No such file or directory: {}".format(path)
        super(NoSuchFile, self).__init__(self.message, *args, **kwargs)


class GCSFS(GenericFS):

    project = Unicode(help="GCP Project", allow_none=True, default_value=None).tag(
        config=True, env="JPYNB_GCS_PROJECT"
    )
    token = Unicode(
        help="Path to the GCP token", allow_none=True, default_value=None
    ).tag(config=True, env="JPYNB_GCS_TOKEN_PATH")

    region_name = Unicode("us-east-1", help="Region name").tag(
        config=True, env="JPYNB_GCS_REGION_NAME"
    )
    bucket = Unicode("notebooks", help="Bucket name to store notebooks").tag(
        config=True, env="JPYNB_GCS_BUCKET"
    )

    prefix = Unicode("", help="Prefix path inside the specified bucket").tag(
        config=True
    )
    separator = Unicode("/", help="Path separator").tag(config=True)

    dir_keep_file = Unicode(
        ".gcskeep", help="Empty file to create when creating directories"
    ).tag(config=True)

    def __init__(self, log, **kwargs):
        super(GCSFS, self).__init__(**kwargs)
        self.log = log

        # token = os.path.expanduser(self.token)
        # self.fs = gcsfs.GCSFileSystem(project=self.project, token=token)
        self.url = 'http://127.0.0.1:5000' 
        self.init()

    def init(self):
        self.mkdir("")
        self.ls("")
        assert self.isdir(""), "The root directory should exists :)"

    #  GenericFS methods -----------------------------------------------------------------------------------------------

    def ls(self, path):
        # Get List of files via api
        path_ = self.path(path)
        import pdb; pdb.set_trace()
        self.log.debug("gcscontents.GCSFS: Listing directory: `%s`", path_)
        response = requests.get(self.url + '/api/contents')
        return response.json()

    def isfile(self, path):
        if path.strip('/') and path.startswith('/') and not os.path.isdir('.ipynb_checkpoints'+path):
            response = requests.post(self.url + '/api/contents/upload/'+path.strip('/'))
            os.system("mkdir -p .ipynb_checkpoints/"+path.strip('/'))
            if not os.path.isfile(".ipynb_checkpoints/"+path.strip('/').replace('.ipynb', '-checkpoint.ipynb')):
                os.system("touch .ipynb_checkpoints/"+path.strip('/').replace('.ipynb', '-checkpoint.ipynb'))
            return False
        if 'ipynb' in path and (not path.startswith('/') or os.path.isdir('.ipynb_checkpoints'+path)):
            return True
        return False

    def isdir(self, path):
        # # GCSFS doesnt return exists=True for a directory with no files so
        # # we need to check if the dir_keep_file exists
        # is_dir = self.isfile(path + self.separator + self.dir_keep_file)
        # path_ = self.path(path)
        # self.log.debug("gcscontents.GCSFS: `%s` is a directory: %s", path_, is_dir)
        # return is_dir
        if 'ipynb' in path:
            return False
        return True

    def mv(self, old_path, new_path):
        # self.log.debug("gcscontents.GCSFS: Move file `%s` to `%s`", old_path, new_path)
        # self.cp(old_path, new_path)
        # self.rm(old_path)
        return True

    def cp(self, old_path, new_path):
        # old_path_, new_path_ = self.path(old_path), self.path(new_path)
        # self.log.debug("gcscontents.GCSFS: Coping `%s` to `%s`", old_path_, new_path_)
        # if self.isdir(old_path):
        #     old_dir_path, new_dir_path = old_path, new_path
        #     for obj in self.ls(old_dir_path):
        #         old_item_path = obj
        #         new_item_path = old_item_path.replace(old_dir_path, new_dir_path, 1)
        #         self.cp(old_item_path, new_item_path)
        # elif self.isfile(old_path):
        #     self.fs.copy(old_path_, new_path_)
        return True

    def rm(self, path):
        # path_ = self.path(path)
        # self.log.debug("gcscontents.GCSFS: Removing: `%s`", path_)
        # if self.isfile(path):
        #     self.log.debug("gcscontents.GCSFS: Removing file: `%s`", path_)
        #     self.fs.rm(path_)
        # elif self.isdir(path):
        #     self.log.debug("gcscontents.GCSFS: Removing directory: `%s`", path_)
        #     dirs = self.fs.walk(path_)
        #     for dir in dirs:
        #         for file in dir[2]:
        #             self.fs.rm(dir[0] + self.separator + file)
        return True

    def mkdir(self, path):
        # path_ = self.path(path, self.dir_keep_file)
        # self.log.debug("gcscontents.GCSFS: Making dir (touch): `%s`", path_)
        # self.fs.touch(path_)
        return True

    def read(self, path, format):
        path_ = self.path(path)
        if not self.isfile(path):
            raise NoSuchFile(path_)
        # with self.fs.open(path_, mode="rb") as f:
        #     content = f.read()
        # if format == "base64":
        #     return base64.b64encode(content).decode("ascii"), "base64"
        # else:
        #     # Try to interpret as unicode if format is unknown or if unicode
        #     # was explicitly requested.
        #     try:
        #         return content.decode("utf-8"), "text"
        #     except UnicodeError:
        #         if format == "text":
        #             err = "{} is not UTF-8 encoded".format(path_)
        #             self.log.error(err)
        #             raise HTTPError(400, err, reason="bad format")
        data = requests.get(self.url + '/api/contents/' + path)
        content = data.json()
        if path.strip('/'):
            os.system("mkdir -p .ipynb_checkpoints/"+path.strip('/'))
            if not os.path.isfile(".ipynb_checkpoints/"+path.strip('/').replace('.ipynb', '-checkpoint.ipynb')):
                os.system("touch .ipynb_checkpoints/"+path.strip('/').replace('.ipynb', '-checkpoint.ipynb'))
        return content
     

    def lstat(self, path):
        # path_ = self.path(path)
        # info = self.fs.info(path_)
        # ret = {}
        # if "updated" in info:
        #     ret["ST_MTIME"] = info["updated"]
        # return ret
        return True

    def write(self, path, content, format):
        path_ = self.path(self.unprefix(path))
        self.log.debug("gcscontents.GCSFS: Writing file: `%s`", path_)
        # with self.fs.open(path_, mode="wb") as f:
        #     if format == "base64":
        #         b64_bytes = content.encode("ascii")
        #         content_ = base64.b64decode(b64_bytes)
        #     else:
        #         content_ = content.encode("utf8")
        #     f.write(content_)
        path = '/'+ path if not path.startswith('/') else path
        response = requests.post(self.url + '/api/contents' + path, data=content)
        if response:
            return True
        return False

    #  Utilities -------------------------------------------------------------------------------------------------------

    def strip(self, path):
        if isinstance(path, str):
            return path.strip(self.separator)
        if isinstance(path, (list, tuple)):
            return list(map(self.strip, path))

    def join(self, *paths):
        paths = self.strip(paths)
        return self.separator.join(paths)

    def get_prefix(self):
        """Full prefix: bucket + optional prefix"""
        prefix = self.bucket
        if self.prefix:
            prefix += self.separator + self.prefix
        return prefix

    prefix_ = property(get_prefix)

    def unprefix(self, path):
        """Remove the self.prefix_ (if present) from a path or list of paths"""
        path = self.strip(path)
        if isinstance(path, str):
            path = path[len(self.prefix_) :] if path.startswith(self.prefix_) else path
            path = path[1:] if path.startswith(self.separator) else path
            return path
        if isinstance(path, (list, tuple)):
            path = [
                p[len(self.prefix_) :] if p.startswith(self.prefix_) else p
                for p in path
            ]
            path = [p[1:] if p.startswith(self.separator) else p for p in path]
            return path

    def path(self, *path):
        """Utility to join paths including the bucket and prefix"""
        path = list(filter(None, path))
        path = self.unprefix(path)
        items = [self.prefix_] + path
        return self.join(*items)
