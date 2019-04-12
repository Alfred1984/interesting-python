import itchat
import pandas as pd


class GroupMember(object):

    @staticmethod
    def get_group_members():
        itchat.auto_login(hotReload=True)
        itchat.dump_login_status()
        room = itchat.search_chatrooms(name=u'xxxxxxx')
        gsq = itchat.update_chatroom(room[0]['UserName'], detailedMember=True)
        members = pd.DataFrame(gsq['MemberList'])
        members.to_csv('groupmembers.csv', index=False)

        print('Successfully saved group members information to csv file!')


if __name__ == '__main__':
    group = GroupMember()
    group.get_group_members()
