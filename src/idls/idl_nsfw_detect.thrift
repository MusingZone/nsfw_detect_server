/*
* NSFW_DETECTION_SERVER IDL
* input:
* output:
*
* 20220312
*/

namespace py nsfw_detection

// ========   Request  ==========

enum RequestType {
	NSFW_DETECT,
	DETECT_DEBUG
}

enum FileType {
	VIDEO,
	IMAGE,
	AUDIO,
	TEXT
}

struct Request {
	1: required RequestType         req_type;
	2: required FileType            file_type;
	3: required list<string>        file_urls;
	4: optional map<string, string> detect_params;
}

// ========    Result  ===========
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

// ======   Exception ==========
exception RequestException {
	1: required i32     code;
	2: optional string  excp;
}

// =======   Service  ===========
service NsfwDetectService {
	// service function
	SearchResult doNsfwDetect(1: Request request) throws(1:RequestException qe);
}
