# coding: utf-8

import sys
# my custom utility
from util.util import *
from nd_helper import *
from idls.nd_idl.nsfw_detection.ttypes import *


# type分流到helper
class NsfwDetectServiceHandler:

    def doNsfwDetect(self, req):
        ndlogger.debug("Get one request")
        start = datetime.datetime.now()

        self._debugInfo(req)

        # search function
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
        nd_helper = NDHelper(nd_conf, req, True)
        detect_result = nd_helper.QP_Access()

        #ndlogger.debug(qpRslt)

        # SResult = nd_helper.IS_Access()
        #
        # RespStatus = ResponseStatus.DETECT_OK
        # RespInfo = ResponseInfo([], [])
        #
        # SResult = SearchResult(RespStatus, RespInfo)
        #
        # ndlogger.debug(SResult)

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
