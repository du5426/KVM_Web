from django.shortcuts import render
from dev_manage.models import NodeInfo
import re
import os
from django.db.models import Max

# Create your views here.

def index(request):
    # server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # 初始化数据库中所有设备的状态置为 “离线”
    node_list = NodeInfo.objects.all()

    # RxNode_InfoFile.txt 文件
    #当存储接收端编号的文件存在时只需要更新数据库中的离线状态
    if os.access("../RxNode_InfoFile.txt", os.F_OK):
        for node in node_list:
            node.node_Status = "离线"
            node.save()
    else:  #当存储接收端的文件不存在时更新离线状态的同时，将Rx设备信息写入文件 RxNode_InfoFile.txt 中
        for node in node_list:
            node.node_Status = "离线"
            if node.node_Type == 'Client':
                with open("../RxNode_InfoFile.txt", "a") as rf:
                    rf.write("Num_" + node.node_Num + "  MAC = " + node.node_MAC + "\n")
            node.save()

    # Search_DevList文件中存储服务器搜索设备后的结果
    if os.access("../Search_DevList.txt",os.F_OK):
        print("Open the Search_DevList.txt")
        # 读取项目文件夹上层文件夹的MacList_Rx.txt，其中存储Qt程序读取到的设备信息
        with open("../Search_DevList.txt", "r") as f:
            all_content = (f.readlines())  # 读取所有数据

        for i in range(0, len(all_content)):

            line_content = all_content[i]  # 读取每一行数据

            local_node_mac = "".join(re.findall('.{2}:.{2}:.{2}:.{2}:.{2}:.{2}', line_content))  # 搜索MAC地址

            if local_node_mac == '':  # 遇到空行则跳过
                continue

            # 当获取到Host设备并且Host列表为空时,直接添加设备
            if line_content.find("Host") >= 0 and NodeInfo.objects.filter(node_Type='Host').count() == 0:
                local_node_num = 1
                local_node_ip = "".join(re.findall('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', line_content))

                NodeInfo.objects.create(node_Num=local_node_num, node_IP=local_node_ip, node_MAC=local_node_mac,node_Status="在线", node_Type="Host")

                with open("../Node_ConfigFile.txt", "a") as node_rf:
                    node_rf.write("Num_1  MAC = " + local_node_mac + "  Operation = Init" + "\n")

            # 当获取到Client设备并且Client列表为空时,直接添加设备
            elif line_content.find("Client") >= 0 and NodeInfo.objects.filter(node_Type='Client').count() == 0:
                local_node_num = 1
                local_node_ip = "".join(re.findall('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', line_content))

                NodeInfo.objects.create(node_Num=local_node_num, node_IP=local_node_ip, node_MAC=local_node_mac,node_Status="在线", node_Type="Client")
                # 接收端信息写入文件 RxNode_InfoFile.txt
                rx_info_f = open("../RxNode_InfoFile.txt", "w")
                rx_info_f.write("Num_1  MAC= " + local_node_mac + "\n")
                rx_info_f.close()

                with open("../Node_ConfigFile.txt", "a") as node_rf:
                    node_rf.write("Num_1  MAC = " + local_node_mac + "  Operation = Init" + "\n")
            # 当设备列表不为空时首先判断列表中是否存在此设备,不存在则添加
            else:
                node_list = NodeInfo.objects.all()
                flag = 1
                # 判断本地MAC地址是否存在数据库中，存在则flag=0 (不添加到数据库),并且设置状态为在线
                for node in node_list:
                    if node.node_MAC == local_node_mac:
                        node.node_Status = "在线"
                        node.save()
                        flag = 0
                        break
                # 若当前MAC不在数据库中，则将当前设备添加到数据库中
                if flag == 1:
                    # local_node_num = int(NodeInfo.objects.all().aggregate(Max('node_Num')).get('node_Num__max')) + 1
                    local_node_ip = "".join(re.findall('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', line_content))

                    if line_content.find("Host") >= 0:
                        local_node_type = "Host"
                        local_node_num = int(NodeInfo.objects.all().filter(node_Type='Host').aggregate(Max('node_Num')).get('node_Num__max')) + 1

                    elif line_content.find("Client") >= 0:
                        local_node_type = "Client"
                        local_node_num = int(NodeInfo.objects.all().filter(node_Type='Client').aggregate(Max('node_Num')).get('node_Num__max')) + 1
                        # 接收端信息写入文件 RxNode_InfoFile.txt
                        rx_info_f = open("../RxNode_InfoFile.txt", "a")
                        rx_info_f.write("Num_" + str(local_node_num) + "  MAC = " + local_node_mac + "\n")
                        rx_info_f.close()

                    NodeInfo.objects.create(node_Num=local_node_num, node_IP=local_node_ip, node_MAC=local_node_mac,node_Status="在线", node_Type=local_node_type)

                    # 将新发现的节点写入Node_Rx_Configure_File.txt中，其中标注好需要进行的操作，以方便C++程序根据此文件对节点进行操作
                    # 注意此处Num_*要前不要有空格或者其他字符，Num_后紧跟字符
                    with open("../Node_ConfigFile.txt", "a") as node_rf:
                        node_rf.write("Num_" + str(local_node_num) + "  MAC = " + local_node_mac + "  Operation = Init" + "\n")

    post_list = NodeInfo.objects.all()

    # server_socket.close()

    return render(request,'index.html',{'post_list':post_list})

def roomManage(request):

    post_list = NodeInfo.objects.all()

    return render(request,"roomManage.html",{'post_list':post_list})


