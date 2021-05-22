from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])


class Appointment(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    customer_name = models.CharField(max_length=50, blank=False)
    employee_name = models.CharField(max_length=50, blank=False)
    appointment_datetime = models.DateTimeField(blank=True, null=True)
    owner = models.ForeignKey('auth.User', related_name='appointments', on_delete=models.CASCADE)
    highlighted = models.TextField()
    # highlighted = models.DateTimeField()

    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)
    # style = models.DateTimeField()

    def save(self, *args, **kwargs):
        # pygments will highlight the HTML
        lexer = get_lexer_by_name(self.language)
        linenos = 'table' if self.linenos else False

        # options = {'customer_name': self.customer_name} if self.customer_name else {}
        options = {}
        # options += {'customer_name': self.customer_name} if self.customer_name else {}
        options += {'employee_name': self.employee_name} if self.employee_name else {}
        # options += {'appointment_datetime': self.appointment_datetime} if self.appointment_datetime else {}

        formatter = HtmlFormatter(style=self.style, linenos=linenos, full=True, **options)
        self.highlighted = highlight(self.employee_name, lexer, formatter)
        super(Appointment, self).save(*args, **kwargs)

    class Meta:
        ordering = ['employee_name']
