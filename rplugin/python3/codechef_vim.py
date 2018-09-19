import os
import neovim
import codechef_cli
import tempfile


@neovim.plugin
class Codechef:
    contest = None

    def __init__(self, nvim):
        self.nvim = nvim

    @neovim.command('CodechefSelectContest', range='', nargs='*')
    def select_contest(self, args, range):
        # TODO: status should be argument
        contests = codechef_cli.api.get_data('contests', params={
            'fields': 'code, name, startDate, endDate',
            'limit': 50,
            'status': 'past'
        })['contestList']
        contests = [contest['code'] + ' - ' + contest['name']
                    for contest in contests]
        self.nvim.call("fzf#run", {'source': contests,
                                   'sink': 'CodechefContestPage',
                                   'down': '30%'})

    @neovim.command('CodechefContestPage', range='', nargs='*', sync=True)
    def contest_page(self, args, range):
        contest_code = str(args[0].split('-')[0].strip())
        filename = tempfile.NamedTemporaryFile().name

        self.contest = codechef_cli.api.get_contest(contest_code)

        body = [
            '┌─────────────────────┐',
            '│       CODECHEF      │',
            '└─────────────────────┘',
            '',
            '',
        ]

        body += self.contest.problem_codes

        self.nvim.funcs.execute('vsplit')
        self.new_buffer_and_append(
            filename, body)

    @neovim.command('CodechefOpenProblem', range='', nargs='*')
    def open_problem(self, args, range):
        if not args:
            idx = self.contest.problem_codes.index(
                self.nvim.current.line.strip())
        else:
            idx = self.contest.problem_codes.index(args[0])
        self.clear_current_buffer_and_write(['Loading...'])
        problem = self.contest[idx]

        body = codechef_cli.util.html_to_terminal(problem.body)
        filename = tempfile.NamedTemporaryFile().name
        self.clear_current_buffer_and_write(
            [problem.problem_name, ''] + body.split('\n')
        )

    @neovim.function('CodechefOpenOldContest')
    def open_old_contest(self, args):
        self.clear_current_buffer_and_write(self.contest.problem_codes)

    def clear_current_buffer_and_write(self, li):
        self.nvim.funcs.execute('setlocal noro')
        self.nvim.funcs.execute("1,$d")
        self.nvim.current.buffer.append(li)
        self.nvim.funcs.execute('w')
        self.nvim.funcs.execute('setlocal ro')

    def new_buffer_and_append(self, filename, li):
        self.nvim.funcs.execute('e ' + filename)
        self.clear_current_buffer_and_write(li)
        self.nvim.funcs.execute('setlocal ft=codechef')
        self.nvim.funcs.execute('setlocal nobuflisted')
