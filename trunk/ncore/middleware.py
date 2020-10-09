# lib
import opentracing
from django.conf import settings
from jaeger_client import Config


class DjangoJaegerMiddleware:
    """
    This middleware uses the Jaeger Python client library to implement tracing in Django at the middleware level.

    This means that every request through the system will be traced.

    The middleware also attaches the parent span to the request object, which allows for child spans to be created
    using `request.span`.
    """

    def __init__(self, get_response):
        """
        This method is run once when the web server receives its first request.
        In it we will set up our tracer instance using conf from the settings file.
        :param get_response: A method that takes a request and passes it down the middleware chain
        """
        self.get_response = get_response
        config = Config(config=settings.TRACER_CONFIG, service_name=settings.TRACER_SERVICE_NAME, validate=True)
        tracer = config.initialize_tracer() or opentracing.tracer
        settings.TRACER = tracer
        self.tracer = tracer

    def __call__(self, request):
        """
        This method is run for every request.
        We will use this method to start a span around the entire request, and attach the span object to the request.

        The method will check if a span has been sent in the headers already, and if so will continue that span, or
        else it will start a new span instead.
        :param request: The user's request
        """
        # strip headers for trace info
        headers = {}
        for k,v in request.META.items():
            k = k.lower().replace('_','-')
            if k.startswith('http-'):
                k = k[5:]
            headers[k] = v

        # Try to start a new span from the trace info
        span = None
        name = '{} {}'.format(request.method, request.get_full_path().lstrip('/').split('?')[0])
        try:
            span_ctx = self.tracer.extract(opentracing.Format.HTTP_HEADERS, headers)
            span = self.tracer.start_span(name, child_of=span_ctx)
        except (opentracing.InvalidCarrierException, opentracing.SpanContextCorruptedException) as e:
            # Start a completely new span
            span = self.tracer.start_span(name)
        if span is None:
            # Shouldn't be but we'll check anyway
            span = self.tracer.start_span(name)

        # Attach the span to the request and do the actual view code
        request.span = span
        response = self.get_response(request)

        # Close the span and return the response
        span.set_tag('status', response.status_code)  # Add status code as tag before finishing
        span.finish()
        return response

