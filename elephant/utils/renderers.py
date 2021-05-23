import json

from rest_framework.compat import INDENT_SEPARATORS, LONG_SEPARATORS, SHORT_SEPARATORS
from rest_framework.renderers import JSONRenderer

from elephant import local
from elephant import constants


class APIRenderer(JSONRenderer):

    ALLOWED_METHODS = ('GET', 'POST', 'PUT', 'DELETE',)

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Render `data` into JSON, returning a bytestring.
        """
        if data is None:
            return bytes()
        renderer_context = renderer_context or {}
        indent = self.get_indent(accepted_media_type, renderer_context)

        if indent is None:
            separators = SHORT_SEPARATORS if self.compact else LONG_SEPARATORS
        else:
            separators = INDENT_SEPARATORS
        response_code = renderer_context["response"].status_code
        cleaned_data = {}
        field = ''
        code = None
        if renderer_context["request"].method in self.ALLOWED_METHODS:
            if response_code >= 200 and response_code < 300:
                cleaned_data['errorCode'] = constants.ALL_OK
                cleaned_data['success'] = True
                cleaned_data["data"] = data
                cleaned_data["showType"] = None
                cleaned_data["traceId"] = local.request_id
                cleaned_data['errorMessage'] = None
            else:
                error_message = None
                if isinstance(data, str):
                    error_message = data
                elif isinstance(data, list):
                    for error in data:
                        error_message = str(error)
                        break
                elif isinstance(data, dict):
                    for k, v in data.items():
                        field = k
                        if isinstance(v, list):
                            v = v[0]
                        error_message, code = constants.REST_ERROR_CODE_MAP.get(v.code, (None, None))
                        if not error_message:
                            error_message = str(v)
                        break
                else:
                    print(data)
                    raise
                cleaned_data["data"] = None
                cleaned_data['success'] = False
                cleaned_data['errorMessage'] = error_message
                cleaned_data["showType"] = 2
                cleaned_data["traceId"] = local.request_id
                cleaned_data['errorCode'] = code or constants.CODE_MSG_MAP.get(error_message, constants.UNKNOWN_ERROR)
                if field and field not in {'detail', 'non_field_errors'}:
                    cleaned_data['errorMessage'] = f'{field}: {error_message}'
        else:
            cleaned_data["data"] = data

        ret = json.dumps(
            cleaned_data, cls=self.encoder_class,
            indent=indent, ensure_ascii=self.ensure_ascii,
            separators=separators
        )
        renderer_context["response"].status_code = 200  # always return 200 http code

        # We always fully escape \u2028 and \u2029 to ensure we output JSON
        # that is a strict javascript subset.
        # See: http://timelessrepo.com/json-isnt-a-javascript-subset
        ret = ret.replace('\u2028', '\\u2028').replace('\u2029', '\\u2029')
        return ret.encode()
