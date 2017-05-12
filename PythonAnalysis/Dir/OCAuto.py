# -*- coding: utf-8 -*-
# ---------------------------------------
#   程序：iOS app auto
#   版本：1.0
#   作者：zhong
#   日期：2017-05-09
#   语言：Python 2.7
# ---------------------------------------

URI = 'https://nj02all02.baidupcs.com/file/b6b00069541e959360f9c75c6a225b83?bkt=p3-1400b6b00069541e959360f9c75c6a225b83dfc4573400000000b564&fid=4010289530-250528-975010193180837&time=1494318606&sign=FDTAXGERLBHS-DCb740ccc5511e5e8fedcff06b081203-LCvx8cYl5UnjYJarbwfPIYZ3AEk%3D&to=70&size=46436&sta_dx=46436&sta_cs=0&sta_ft=zip&sta_ct=0&sta_mt=0&fm2=MH,Guangzhou,Netizen-anywhere,,guangdong,ct&newver=1&newfm=1&secfm=1&flow_ver=3&pkey=1400b6b00069541e959360f9c75c6a225b83dfc4573400000000b564&sl=75300943&expires=8h&rt=pr&r=720949158&mlogid=2984628044235289627&vuk=4010289530&vbdid=3052596471&fin=SZExample.zip&fn=SZExample.zip&rtype=1&iv=1&dp-logid=2984628044235289627&dp-callid=0.1.1&hps=1&csl=418&csign=4nv66jMqsxCvXGAk0lWhAKgeORo%3D&by=themis'
FLI = '/Users/wushengzhong/Desktop/valid/SZEnum'

import zipfile
import os
import arrow
import numpy
import uuid

project_name = "SZEnum"
arr = ['project.pbxproj',
       'xcschememanagement.plist']

# 解压文件
def un_zip(file_name, path):
    """unzip zip file"""
    zip_file = zipfile.ZipFile(file_name)
    if os.path.isdir(path):
        pass
    else:
        os.mkdir(path)
    for names in zip_file.namelist():
        zip_file.extract(names, path)
    zip_file.close()

# ======================================================================================================================
# 创建工程
# ======================================================================================================================

# 创建工程
# ==> 思路: 从一个现有的工程修改名字到新工程
def create_proj(path, name, oldname):
    un_zip('/Users/wushengzhong/Desktop/valid/SZExample.zip', path)
    # 修改文件内容 修改该文件名
    project_name = name
    arr.append(oldname+'.xcscheme')
    modify_file(path, name, oldname)
    modify_folder(path, name, oldname)


# 修改该文件名
def modify_file(path, name, oldname):
    for rt, dirs, files in os.walk(path):
        for f in files:
            if f in arr:
                replace(rt + '/' + f, name, oldname)
            if f.find(oldname) != -1:
                newname = f.replace(oldname, name)
                os.rename(os.path.join(rt, f), os.path.join(rt, newname))
        for dir in dirs:
            modify_file(dir, name, oldname)


# 修改该文件夹名
def modify_folder(path, name, oldname):
    for rt, dirs, files in os.walk(path):
        for dir in dirs:
            modify_folder(dir, name, oldname)
            if dir.find(oldname) != -1:
                newname = dir.replace(oldname, name)
                os.rename(os.path.join(rt, dir), os.path.join(rt, newname))


# 替换文件中的名字
def replace(path, name, oldname):
    with open(path, 'r') as f:
        lines = f.readlines()
    with open(path, 'w') as w:
        [w.write(i.replace(oldname, name)) for i in lines]

# ======================================================================================================================
# 生成文件, 导入文件
# ======================================================================================================================

# 思路:
# ==> a. 先生成指定文件
#     b. 导入文件到指定位置
#     c. 添加引用到工程文件
#        a. 添加到  PBXBuildFile section
#           e.g. BD043F991EC1C706009BA58E /* UFQViewController.m in Sources */ = {isa = PBXBuildFile; fileRef = BD043F981EC1C706009BA58E /* UFQViewController.m */; };
#        b. 添加到  PBXFileReference section
#           e.g. BD043F971EC1C706009BA58E /* UFQViewController.h */ = {isa = PBXFileReference; fileEncoding = 4;
#                    lastKnownFileType = sourcecode.c.h; path = UFQViewController.h; sourceTree = "<group>"; };
#                BD043F981EC1C706009BA58E /* UFQViewController.m */ = {isa = PBXFileReference; fileEncoding = 4;
#                    lastKnownFileType = sourcecode.c.objc; path = UFQViewController.m; sourceTree = "<group>"; };
#        c. 添加到 PBXGroup section  指定组, 如果没有组则添加组
#           e.g. BD043F981EC1C706009BA58E /* UFQViewController.m */
#                BD043F971EC1C706009BA58E /* UFQViewController.h */
#        d. 添加到 PBXSourcesBuildPhase section
#           e.g. BD043F991EC1C706009BA58E /* UFQViewController.m in Sources */

# 创建工程
# create_proj('/Users/wushengzhong/Desktop/valid/SZEnum', 'SZEnum', 'SZExample')
#

# ======================================================================================================================
# 生成View
# ======================================================================================================================

def create_view(path, name, list):
    if os.path.exists(path) == False:
        os.makedirs(path)
    create_view_h(path, name)
    create_view_m(path, name, list)

# 创建.h 文件
def create_view_h(path, name):
    file_path = path + '/' + name + '.h'
    create_file(file_path, h_file(name))

def create_view_m(path, name, list):
    file_path = path + '/' + name + '.m'
    create_file(file_path, m_file(name, list))

def create_file(path, list):
    with open(path, 'w') as w:
        [w.write(i) for i in list]

# ======================================================================================================================
# 生成ViewController
# ======================================================================================================================

def create_vc(path, name, list):
    if os.path.exists(path) == False:
        os.makedirs(path)
    create_vc_h(path, name)
    create_vc_m(path, name, list)

def create_vc_h(path, name):
    file_path = path + '/' + name + '.h'
    create_file(file_path, h_vc_file(name))

def create_vc_m(path, name, list):
    file_path = path + '/' + name + '.m'
    create_file(file_path, m_vc_file(name, list))

# ======================================================================================================================
# .h 文件
# ======================================================================================================================

def h_file(name):
    return note(name) + h_static(name)

def h_vc_file(name):
    return note(name) + h_vc_static(name)

# 注释部分
def note(name):
    return ['//\n',
            '//  %s\n' % name,
            '//  %s\n' % project_name,
            '//\n',
            '//  Created by wushengzhong on %s.\n' % arrow.now().format('YYYY/MM/DD'),
            '//\n\n']


def p_note(name):
    return ['#pragma mark - %s\n' % name,
            '///=============================================================================\n',
            '/// @name %s\n' % name,
            '///=============================================================================\n\n']

# h文件
def h_static(name):
    return ['#import <UIKit/UIKit.h>\n\n',
            '@interface %s : UIView<ViewDelegate>\n\n' % name,
            '@end\n']


def h_vc_static(name):
    return ['#import <UIKit/UIKit.h>\n\n',
            '@interface %s : UIViewController<RouterDataDelegate>\n\n' % name,
            '@end\n']

# ======================================================================================================================
# .m
# ======================================================================================================================

def m_file(name, list):
    return note(name) + m_h(name, list) + vd(name) + view(list) + layout(list) + getter(list) + m_end()

def m_vc_file(name, list):
    return note(name) + m_h(name, list) + vd_vc(name) + vc(list) + vc_layout(list) + getter(list) + m_end()

# ======================================================================================================================
# .m  头部
# ======================================================================================================================

# 总
def m_h(name, list):
    return m_h_begin(name, list) + m_h_param(list) + m_h_param_inherent() + m_end() + m_implent(name)

def m_vc_h(name, list):
    return m_h_begin(name, list) + m_h_param(list) + m_h_vc_param_inherent() + m_end() + m_implent(name)

def m_h_begin(name, list):
    arr = ['#import "%s"\n\n\n' % name,
            '@interface %s ()\n' % name]
    for t in [t for t in list if t[0] == 'tab']:
        str = '#define CellClass @"%sCell"\n' % t[1]
        arr.insert(1, str)
    if len(arr) >= 2:
        arr.insert(-1, '\n')
    return arr

def m_h_param(list):
    arr = [param_identifier(t) for t in list]
    return [y for x in arr for y in x]
# para
def param_identifier((ptype, name, note)):
    return ['/*! %s */\n' % note,
            '@property (nonatomic, strong) %s *%s;\n' % (p_type(ptype), name)]

def m_h_param_inherent():
    return ['\n#pragma mark - inherent\n',
            '/*!  */\n',
            '@property (nonatomic, copy) SZActionBlock actionBlock;\n',
            '/*!  */\n',
            '@property (nonatomic, strong) id model;\n']

def m_h_vc_param_inherent():
    return ['/*!  */\n',
            '@property (nonatomic, strong) id model;\n']

def m_end():
    return ['@end\n\n']

def p_type(type):
    return {'img' : 'UIImageView',
            'txt' : 'UILabel',
            'btn' : 'UIButton',
            'tab' : 'UITableView',
            'view' : 'UIView'}[type]

# @implentment
def m_implent(name):
    return ['@implementation %s\n\n' % name]

# ======================================================================================================================
# ViewDelegate 部分
# ======================================================================================================================

# 总
def vd(name):
    return p_note('ViewDelegate') + vd_instance()

def vd_vc(name):
    return p_note('RouterDataDelegate') + vc_router()

def vd_instance():
    return ['+ (instancetype)viewWithModel:(id)model action:(SZActionBlock)action {\n',
            '    return [[self alloc] initWithFrame:CGRectZero model:model action:action];\n',
            '}\n\n']

def vc_router():
    return ['- (void)routerPassParamters:(RACTuple *)tuple {\n',
            '    self.model = tuple.first;\n',
            '}\n\n']

# ======================================================================================================================
# View 部分
# ======================================================================================================================

# 总
def view(list):
    return p_note('View') + view_init() + ['- (void)addViews {\n'] + view_add(list) + ['}\n\n']

def vc(list):
    return p_note('VCLife') + vc_viewdidload() + p_note('LoadData') + vc_loaddata() +  p_note('View') + ['- (void)addViews {\n'] + vc_add(list) + ['   [self updateLayout];\n', '}\n\n']

def vc_viewdidload():
    return ['- (void)viewDidLoad {\n',
            '    [super viewDidLoad];\n',
            '    self.title = @"我是标题";\n',
            '    self.view.backgroundColor = SZHexColor(f0f3f5);\n',
            '    [self loadData];\n',
            '}\n\n']

def vc_loaddata():
    return ['- (void)loadData {\n',
            '    [self showProgressHud:YES];\n',
            '    @weakify(self);\n',
            '    [[SZRequest request].urlString(@"/firstPage/rcmdList")\n',
            '    .paramaters(@{})\n',
            '    .szTask szContinueBlock:^id(BFTask *t, JSONModel *result) {\n',
            '        @strongify(self);\n',
            '        if (t.error) {\n\n',
            '        } else {\n',
            '            self.model = result.data;\n',
            '            [self configData];\n',
            '        }\n',
            '        return nil;\n',
            '    }];\n',
            '}\n\n',
            '- (void)configData {\n',
            '    [self addView];\n',
            '}\n\n']

def view_init():
    return ['- (instancetype)initWithFrame:(CGRect)frame model:(id)model action:(SZActionBlock)action {\n',
            '    if (self = [super initWithFrame:frame]) {\n',
            '        self.actionBlock = action;\n',
            '        self.model = model;\n',
            '        self.backgroundColor = SZHexColor(ffffff);\n',
            '        [self addViews];\n',
            '    }\n',
            '    return self;\n',
            '}\n\n']

def view_add(list):
    return ['   [self addSubview:self.%s]\n' % name for (ptype, name, note) in list]

def vc_add(list):
    return ['   [self.view addSubview:self.%s]\n' % name for (ptype, name, note) in list]

# ======================================================================================================================
# Layout 部分
# ======================================================================================================================

# 总
def layout(list):
    return p_note('Layout') + layout_begin() + layout_view(list) + layout_end()

def vc_layout(list):
    return p_note('Layout') + layout_begin() + layout_view(list) + ['}\n\n']

def layout_begin():
    return ['- (void)updateLayout {\n',
            '    @weakify(self);\n']

def layout_view(list):
    arr = [layout_view_layout(name) for (ptype, name, note) in list]
    return [y for x in arr for y in x]

def layout_view_layout(name):
    return ['    [_%s mas_updateConstraints:^(MASConstraintMaker *make) {\n' % name,
            '        @strongify(self);\n',
            '        make.left.equalTo(self.mas_left).offset(0);\n',
            '        make.top.equalTo(self.mas_top).offset(0);\n',
            '    }];\n']

def layout_end():
    return ['}\n\n',
            '- (void)updateConstraints {\n',
            '    [super updateConstraints];\n',
            '    [self updateLayout];\n',
            '}\n\n',
            '+ (BOOL)requiresConstraintBasedLayout {\n',
            '    return YES;\n',
            '}\n\n']

# ======================================================================================================================
# Layout 部分
# ======================================================================================================================

# Getters 部分
def getter(list):
    return p_note('Getters') + getter_param(list)

def getter_param(list):
    arr = [p_lazy(t) for t in list]
    return [y for x in arr for y in x]

def p_lazy((ptype, name, note)):
    return {'img':lazy_img(name, note),
            'txt':lazy_txt(name, note),
            'btn':lazy_btn(name, note),
            'tab':lazy_tab(name, note),
            'view':lazy_view(name, note)}[ptype]

def lazy_img(name, note):
    return ['/*! %s */\n' % note,
            '- (UIImageView *)%s {\n' % name,
            '    if (!_%s) {\n' % name,
            '        _%s = [UIImageView new];\n' % name,
            '        _%s.image = [UIImage imageNamed:@"arrow"];\n' % name,
            '    }\n',
            '    return _%s;\n' % name,
            '}\n\n']

def lazy_view(name, note):
    return ['/*! %s */\n' % note,
            '- (UIView *)%s {\n' % name,
            '    if (!_%s) {\n' % name,
            '        _%s = [UIView new];\n' % name,
            '        _%s.backgroundColor = SZHexColor(e2e6e9);\n' % name,
            '    }\n',
            '    return _%s;\n' % name,
            '}\n\n']

def lazy_txt(name, note):
    return ['/*! %s */\n' % note,
            '- (UILabel *)%s {\n' % name,
            '    if (!_%s) {\n' % name,
            '        _%s = [[UILabel alloc] init];\n' % name,
            '        _%s.font = [UIFont systemFontOfSize:12];\n' % name,
            '        _%s.textColor = SZHexColor(555555);\n' % name,
            '    }\n',
            '    return _%s;\n' % name,
            '}\n\n']

def lazy_btn(name, note):
    return ['/*! %s */\n' % note,
            '- (UIButton *)%s {\n' % name,
            '    if (!_%s) {\n' % name,
            '        _%s = [UIButton buttonWithType:UIButtonTypeCustom];\n' % name,
            '        [_%s setTitle:@"按钮" forState:UIControlStateNormal];\n' % name,
            '        [_%s setTitleColor:SZHexColor(ffffff) forState:UIControlStateNormal];\n' % name,
            '        _%s.titleLabel.font = [UIFont systemFontOfSize:17];\n' % name,
            '        [[_%s rac_signalForControlEvents:UIControlEventTouchUpInside] subscribeNext:^(UIControl *x) {\n' % name,
            ' \n',
            '        }];\n'
            '    }\n',
            '    return _%s;\n' % name,
            '}\n\n']

def lazy_tab(name, node):
    return ['- (UITableView *)%s {\n' % name,
            '    if (!_%s) {\n' % name,
            '        _%s = [[UITableView alloc] initWithFrame:CGRectMake(0, 0, LSScreenWidth, LSScreenHeight - 64) style:UITableViewStylePlain];\n' % name,
            '        _%s.separatorStyle = UITableViewCellSeparatorStyleNone;\n' % name,
            '        _%s.backgroundColor = SZHexColor(f0f3f5);\n' % name,
            '        [_%s registerClass:NSClassFromString(CellClass) forCellReuseIdentifier:CellClass];\n' % name,
            '    }\n',
            '    return _%s;\n' % name,
            '}\n\n']


create_view(FLI, 'IconView', [('btn', 'selectedBtn', '选择按钮'),
                              ('txt', 'title', '标题'),
                              ('img', 'icon', '图片'),
                              ('txt', 'sub', '子标题'),
                              ('tab', 'tableView', ''),
                              ('view', 'botline', '底线')])
create_view(FLI, 'HomeView', [('btn', 'selectedBtn', '选择按钮'),
                              ('txt', 'title', '标题'),
                              ('img', 'icon', '图片'),
                              ('txt', 'sub', '子标题'),
                              ('tab', 'tableView', ''),
                              ('view', 'botline', '底线')])
create_vc(FLI, 'SZViewController', [('tab', 'tableView', ''),
                                    ('multi', ['IconView', 'HoneView'], [0, 0])])
