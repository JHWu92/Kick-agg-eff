**Unzip data.zip in this directory**

pledge_network_nodes:
        - 以(des, category)为id，比如，第一行表示Ajax, ON, CA在design这个类别下有3个项目，Ajax, ON, CA在photography有1个项目
        - des_%scfl：(des, category)的所有项目中，成功的比例
        - des_total_backer_sum：(des, category)的所有项目中，总共的backers的人次
        - des_total_backer_mean：des_total_backer_sum/des_#projects
        - des_#projects：(des, category)有多少个项目
        - des_$pld_sum：(des, category)所有项目总共筹到的钱，美金为单位
        - des_$pld_mean：des_$pld_sum/des_#projects

pledge_network_edges:
        - 以(src, des, category)为id，比如第2行是总共有1个（src_backers）来自Markham, ON, CA的backers 出现在Ajax, ON, CA的publish项目中的top 10 backers cities中。
        - 其他的字段和pledge_network_nodes相同含义，都是des的属性