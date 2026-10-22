/**
 * 工具函数模块
 */

/**
 * 格式化时长（秒 -> X小时Y分Z秒）
 */
export function formatTime(seconds) {
  const h = Math.floor(seconds / 3600)
  const m = Math.floor((seconds % 3600) / 60)
  const s = seconds % 60
  let result = ''
  if (h > 0) result += `${h}小时`
  if (m > 0 || h > 0) result += `${m}分`
  result += `${s}秒`
  return result
}

/**
 * 获取电影分级中文说明
 */
export function getGradeText(grade) {
  const gradeMap = {
    'G': '大众级',
    'PG': '辅导级',
    'PG-13': '特别辅导级',
    'R': '限制级',
    'NC-17': '17岁以下禁止',
    'NR': '未分级'
  }
  return gradeMap[grade] || grade
}
