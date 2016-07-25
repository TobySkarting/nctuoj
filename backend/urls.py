from utils.include import include
class Handler:
    pass
include(Handler, "./handler/")
urls = [
    (r'/', Handler.index.Index),
    (r'/api/users/', Handler.api.user.Users),
    (r'/api/users/(\d+)/', Handler.api.user.User),
    (r'/api/users/(\d+)/power/', Handler.api.user.Power),
    (r'/api/users/session/', Handler.api.session.Session),

    (r'/api/bulletins/', Handler.api.bulletin.Bulletins),
    (r'/api/bulletins/(\d+)/', Handler.api.bulletin.Bulletin),

    # (r'/api/problems/', Handler.api.problem.problem.Problems),
    # (r'/api/problems/(\d+)/', Handler.api.problem.problem.Problem),
    # (r'/api/problems/(\d+)/rejudge/', Handler.api.problem.rejudge.Rejudge),
    # (r'/api/problems/(\d+)/execute/', Handler.api.problem.execute.Execute),
    # (r'/api/problems/(\d+)/verdict/', Handler.api.problem.verdict.Verdict),
    # (r'/api/problems/(\d+)/testdata/', Handler.api.problem.testdata.Testdata),
    # (r'/api/problems/(\d+)/tag/',     Handler.api.problem.tag.Tag),

    # (r'/api/submissions/', Handler.api.submission.Submissions),
    # (r'/api/submissions/(\d+)/', Handler.api.submission.Submission),
    # (r'/api/submissions/(\d+)/rejudge/', Handler.api.submission.SubmissionRejudge),

    # (r'/api/testdata/', Handler.api.testdata.Testdata),
    # (r'/api/testdata/(\d+)/', Handler.api.testdata.Testdatum),

    # (r'/api/groups/', Handler.api.group.group.Groups),
    # (r'/api/groups/(\d+)/', Handler.api.group.group.Group),
    # (r'/api/groups/(\d+)/members/', Handler.api.group.member.Members),
    # (r'/api/groups/(\d+)/members/(\d+)/', Handler.api.group.member.Member),
    # (r'/api/groups/(\d+)/members/(\d+)/power/', Handler.api.group.member.MemberPower),
    # (r'/api/groups/(\d+)/bulletins/', Handler.api.group.bulletin.Bulletins),
    # (r'/api/groups/(\d+)/problems/', Handler.api.group.problem.Problems),
    # (r'/api/groups/(\d+)/submissions/', Handler.api.group.submission.Submissions),
    # (r'/api/groups/(\d+)/contests/', Handler.api.group.contest.Contests),

    # (r'/api/languages/', Handler.api.language.Languages),
    # (r'/api/languages/(\d+)/', Handler.api.language.Language),

    # (r'/api/executes/', Handler.api.execute.Executes),
    # (r'/api/executes/(\d+)/', Handler.api.execute.Execute),

    # (r'/api/verdicts/', Handler.api.verdict.Verdicts),
    # (r'/api/verdicts/(\d+)/', Handler.api.verdict.Verdict),

    # (r'/api/contests/', Handler.api.contest.contest.Contests),
    # (r'/api/contests/(\d+)/', Handler.api.contest.contest.Contest),
    # (r'/api/contests/(\d+)/problems/', Handler.api.contest.problem.Problems),
    # (r'/api/contests/(\d+)/submissions/', Handler.api.contest.submission.Submissions),
    # (r'/api/contests/(\d+)/scoreboard/', Handler.api.contest.scoreboard.Scoreboard),

    # (r'/api/system/time/', Handler.api.system.time.Time),

    # (r'/api/tags/', Handler.api.tag.Tags),
    # (r'/api/tags/(\d+)/', Handler.api.tag.Tag),

]
