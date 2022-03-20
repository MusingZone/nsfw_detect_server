# coding: utf-8

import sys
# my custom utility
from utils.util import *
from nd_helper.nd_image_helper import *
from nd_helper.nd_video_helper import *
from nd_idl.nsfw_detection.ttypes import *


# type分流到helper
class NsfwDetectServiceHandler:

    def doNsfwDetect(self, req):
        ndlogger.debug("Get one request")
        start = datetime.datetime.now()

        self._debugInfo(req)
        ndlogger.debug("req: ", req)

        # search function

        # 临时构造
        # nd_status = ResponseStatus.DETECT_OK
        # resp_info = ResponseInfo([1.23], ['xxxxx'])
        # ret = SearchResult(nd_status, resp_info)

        ret = self._doNsfwDetect(req)
        ndlogger.debug(ret)

        final_end = datetime.datetime.now()
        ndlogger.debug("Done search, respone time {}".format((final_end - start)))

        return ret

    # 核心操作1 _doNsfwDetect
    def _doNsfwDetect(self, req):

        # step 1. query_process
        # ndlogger.debug("==== Step 1. QP Access         ====")
        #
        # ndlogger.debug("==== Step 1. QP Access Success ====")

        # step 2. vector_search
        # ndlogger.debug("==== Step 2. IS Access         ====")
        # nd_helper = ISHelper(nd_conf, req, qpRslt, True)

        nd_start = datetime.datetime.now()

        # 图像
        if (req.file_type == 0):

            nd_video_helper = NDVideoHelper(nd_conf, req, True)

            detect_result = nd_video_helper.One_Predict()

        elif (req.file_type == 1):

            nd_image_helper = NDImageHelper(nd_conf, req, True)

            detect_result = nd_image_helper.One_Predict()



        nd_end = datetime.datetime.now()
        ndlogger.debug("Done search, respone time {}".format((nd_end - nd_start)))
        ndlogger.debug("==== Step 2. IS Access Success ====")

        # step 3. 拼装结果
        ''' Detect Result
        enum ResponseStatus {
            DETECT_OK,
            ERROR_1
        }
        
        struct ResponseInfo {
            1: required list<double>    detect_result;
            2: optional list<string>    debug_info;
        }
        
        struct SearchResult {
            1: required ResponseStatus  resp_status;
            2: required ResponseInfo    resp_info;
        }
        '''

        nd_status = ResponseStatus.DETECT_OK
        resp_info = ResponseInfo(detect_result, [])
        nd_result = SearchResult(nd_status, resp_info)

        return nd_result

    def _debugInfo(self, req):
        ndlogger.debug(req)
