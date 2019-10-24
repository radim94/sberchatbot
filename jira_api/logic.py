from .test_jira import JIRA_API

from dialog_bot_sdk import interactive_media


class JIRA_UI:

    @staticmethod
    def get_start_buttons():
        return [
            interactive_media.InteractiveMediaGroup(
                [interactive_media.InteractiveMedia(
                    'show_my_issue',
                    interactive_media.InteractiveMediaButton("show_my_issue", "Посмотреть мои задачи")
                )]),
            interactive_media.InteractiveMediaGroup(
                [interactive_media.InteractiveMedia(
                    'add_issue',
                    interactive_media.InteractiveMediaButton("add_issue", "Добавить задачу")
                )])
        ]

    @staticmethod
    def show_issues(options):
        return [interactive_media.InteractiveMediaGroup(
            [interactive_media.InteractiveMedia(
                'select_task',
                interactive_media.InteractiveMediaSelect(options, "Tasks")
            )]),
        ]

    @staticmethod
    def show_transition(transition):
        return [interactive_media.InteractiveMediaGroup(
            [interactive_media.InteractiveMedia(
                'transition',
                interactive_media.InteractiveMediaSelect(transition, "Transition")
            )])]

    @staticmethod
    def show_issues_in_sprint(options):
        return [interactive_media.InteractiveMediaGroup(
            [interactive_media.InteractiveMedia(
                'select_task_in_sprint',
                interactive_media.InteractiveMediaSelect(options, "Tasks")
            )]),
            # interactive_media.InteractiveMediaGroup([
            #     interactive_media.InteractiveMedia(
            #         'back',
            #         interactive_media.InteractiveMediaButton('back', 'Назад')
            #     )
            # ])
        ]
