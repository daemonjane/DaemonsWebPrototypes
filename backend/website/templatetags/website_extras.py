from datetime import datetime

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def status_badge(completed):
    if completed:
        return mark_safe(
            '<span class="inline-flex items-center gap-1 text-emerald-400 text-xs font-medium">'
            '<span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>Done</span>'
        )
    return mark_safe(
        '<span class="inline-flex items-center gap-1 text-slate-500 text-xs font-medium">'
        '<span class="w-1.5 h-1.5 rounded-full bg-slate-600"></span>Pending</span>'
    )


@register.filter
def time_ago(value):
    now = datetime.now(value.tzinfo if value.tzinfo else None)
    diff = now - value
    if diff.days > 365:
        years = diff.days // 365
        return f"{years}y ago"
    if diff.days > 30:
        months = diff.days // 30
        return f"{months}mo ago"
    if diff.days > 0:
        return f"{diff.days}d ago"
    if diff.seconds > 3600:
        hours = diff.seconds // 3600
        return f"{hours}h ago"
    if diff.seconds > 60:
        minutes = diff.seconds // 60
        return f"{minutes}m ago"
    return "just now"


@register.filter
def trim(value):
    if isinstance(value, str):
        return value.strip()
    return value


@register.filter
def field_errors(field):
    return field.errors


@register.filter
def pluralize_count(value, arg="s"):
    if value == 1:
        return f"{value} {arg}" if not arg.endswith("s") else f"{value} {arg[:-1]}"
    return f"{value} {arg}"


@register.simple_tag
def task_stats():
    from ..models import Task
    total = Task.objects.count()
    done = Task.objects.filter(completed=True).count()
    pending = total - done
    return f"{done}/{total} done ({pending} pending)"
