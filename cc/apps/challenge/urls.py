from django.conf.urls import patterns, url

from apps.challenge.views import index, create, detail, maintain, joinleave, rules, comments, entry


urlpatterns = patterns('',
	url(r'^$', index.IndexView.as_view(), name='index'),
	url(r'^create/$', create.CreateView.as_view(), name='create'),

	url(r'^(?P<pk>\d+)/$', detail.DetailView.as_view(), name='detail'),
	url(r'^(?P<pk>\d+)/maintain$', maintain.MaintainView.as_view(), name='maintain'),
	url(r'^(?P<pk>\d+)/join$', joinleave.JoinView.as_view(), name='join'),
	url(r'^(?P<pk>\d+)/leave$', joinleave.LeaveView.as_view(), name='leave'),

	url(r'^add_rule_template/(?P<rule_count>\d+)$', rules.AddRuleTemplate.as_view(), name='add_rule_template'),
	url(r'^(?P<pk>\d+)/update_rule$', rules.UpdateRuleView.as_view(), name='update_rule'),
	url(r'^(?P<pk>\d+)/delete_rule$', rules.DeleteRuleView.as_view(), name='delete_rule'),

	url(r'^(?P<pk>\d+)/submit_comment$', comments.SubmitComment.as_view(), name='submit_comment'),
	url(r'^(?P<pk>\d+)/submit_entry$', entry.SubmitEntry.as_view(), name='submit_entry'),
	url(r'^(?P<pk>\d+)/entry/(?P<epk>\d+)$', entry.EntryDetail.as_view(), name='entry'),
	url(r'^(?P<pk>\d+)/entry/(?P<epk>\d+)/submit_comment$', entry.SubmitEntryComment.as_view(), name='submit_entry_comment'),
	url(r'^(?P<pk>\d+)/entry/(?P<epk>\d+)/submit_ss$', entry.SubmitEntryScreenshot.as_view(), name='submit_entry_screenshot'),
)