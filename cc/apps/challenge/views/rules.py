from django.views import generic
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from ..models import Challenge, Rule
from ..forms import AddRuleTemplateFormset


class UpdateRuleView(generic.View):
    @method_decorator(login_required)
    def post(self, request, pk, *args, **kwargs):
        rule = get_object_or_404(Rule, pk=pk)

        if (rule.challenge.owner == request.user.coder):
            setattr(rule, request.POST['name'], request.POST['value'])
            rule.save()
            return HttpResponse('Rule updated.')
        else:
            return HttpResponse('Can not update a rule for a challenge that you do not own.')


class DeleteRuleView(generic.View):
    @method_decorator(login_required)
    def post(self, request, pk, *args, **kwargs):
        rule = get_object_or_404(Rule, pk=pk)

        if (rule.challenge.owner == request.user.coder):
            rule.delete()
            return HttpResponse('yay')
        else:
            return HttpResponse('Can not delete a rule for a challenge that you do not own.')


class AddRuleTemplate(generic.View):
    template_name = 'challenge/add_rule_template.html'

    @method_decorator(login_required)
    def get(self, request, rule_count, *args, **kwargs):
        rule_formset = AddRuleTemplateFormset(instance=Challenge())

        formset = rule_formset.form(
            auto_id=rule_formset.auto_id,
            prefix=rule_formset.add_prefix(rule_count),
            empty_permitted=True,
        )

        rule_formset.add_fields(formset, None)

        return render(request, self.template_name, { 'rule_formset': formset, 'rule_count': rule_count })

