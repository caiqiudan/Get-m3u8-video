import requests
import os

class M3u8_video():
    '''
    url: m3u8文件网址
    请提前下载好ffmpeg应用
    video_name: 视频名称
    '''
    def __init__(self,url,url_head,video_name):
        self.url = url                           # m3u8的网址
        self.url_head = url_head
        self.urls_name = 'Ding_m3u8_url.txt'     # 存放网址的文件名
        self.urls_path = M3u8_video.get_url(self)  # 存放网址的文件名所在的路径
        self.video_name = video_name             # 最终视频的名字

    # 获得m3u8，保存到当前文件夹下的网址.txt文件
    def get_url(self):
        r = requests.get(self.url)
        with open(self.urls_name,'w') as f:      # 保存到网址.txt
            f.write(r.text)

        path = os.getcwd() + f'\{self.urls_name}'# 路径
        return path

    # 爬取每个网址的数据
    def get_save_data(self):
        m = 1                                    # m表示第m个网址
        with open(self.urls_path,'r') as f:      # 读取网址文件
            for line in f:                       # 遍历文件里的网址
                if len(line) > 50:    			 # 判断当网址为视频网址时
                    url = self.url_head + f'{line.rstrip()}' # 注意用.rstrip()方法去掉\n这个字符，如果时打印出来时发现不了这个问题的
                    jindu = format(m/408,'.2%')  # 百分比进度
                    print(f'正在下载第{m}个片段(进度{jindu})...') # 打印进度
                    r2 = requests.get(url)       # 爬取数据
                    # r2.encoding = 'utf-8'      # 如果数据乱码就解码

                    video_file_path = os.getcwd() + r'\video'
                    if os.path.exists(video_file_path) == False:      # 创建一个名叫video的文件夹用来存放一堆ts视频
                        os.mkdir(video_file_path)

                    with open(fr'.\video\{m}.ts','wb', ) as f:        # 保存到video文件夹里的ts文件，wb:覆盖写入
                        f.write(r2.content)      # 写入数据
                    m += 1
        M3u8_video.filelist(self)                  # 生成filelist
        M3u8_video.concat_video(self)              # 合并为一个文件

    # 生成ts路径，保存到filelist.txt ffmpeg合并视频时要用到
    def filelist(self):
        files = os.listdir(os.getcwd() + r"\video")  # 获取一堆.ts的文件名
        files.sort(key=lambda x: int(x[:-3]))        # 将文件名按数字大销排序
        with open('filelist.txt', 'w') as f:         # 创建filelist.txt文件
            for file in files:
                ts_path = os.getcwd() + r"\video" + f'\{file}'
                data = f"file  '{ts_path}'"          # 写入的格式要符合规范
                f.write(data)
                f.write('\n')

    # 再cmd端用ffmpeg执行ts合并为mp4命令
    def concat_video(self):
        ''''
        video_file_name: 存放一堆ts视频的文件夹名称
        '''
        print('合并视频中...')
        # 一：进入video文件夹，二：合并文件夹里的ts视频,保存再video文件夹里
        order = fr'cd video && ffmpeg -f concat -safe 0 -i ..\filelist.txt -c copy {self.video_name}.mp4'
        os.system(order) # 终端执行命令

if __name__ == '__main__':
    url = 'https://dtliving.alicdn.com/live_hp/5218c5f5-aee1-495c-b213-ef7a48812936_merge.m3u8?auth_key=1605754853-0-0-b505fc6143bd1fa7ba597aa260c6c3c9&cid=3d5aa817528fcbbc837718329b5d8583'
    url_head = 'https://dtliving.alicdn.com/live_hp/'
    m3u8_video = M3u8_video(url,url_head,'回放') # url是m3u8的网址，url_head是视频网址的头, '回放'是爬取视频的名称
    m3u8_video.get_save_data() # 爬取视频并保存再vedio文件夹里
